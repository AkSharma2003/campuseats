import express from "express";
import cors from "cors";
import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@apollo/server/express4";
import { GraphQLError } from "graphql";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { pool, testDatabaseConnection } from "./db.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const typeDefs = await readFile(path.join(__dirname, "schema.graphql"), "utf8");

function toDish(row) {
  if (!row) return null;
  return {
    id: String(row.id),
    name: row.name,
    price: Number(row.price),
    available: Boolean(row.available),
  };
}

const resolvers = {
  Query: {
    dishes: async () => {
      const [rows] = await pool.query(
        "SELECT id, name, price, available FROM dishes ORDER BY id"
      );
      return rows.map(toDish);
    },
    dish: async (_parent, { id }) => {
      const [rows] = await pool.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [Number(id)]
      );
      return toDish(rows[0]);
    },
  },
  Mutation: {
    addDish: async (_parent, { input }) => {
      const [result] = await pool.execute(
        "INSERT INTO dishes (name, price, available) VALUES (?, ?, ?)",
        [input.name, input.price ?? 0, input.available ?? true]
      );
      const [rows] = await pool.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [result.insertId]
      );
      return toDish(rows[0]);
    },
    updateDish: async (_parent, { input }) => {
      const [result] = await pool.execute(
        "UPDATE dishes SET name = ?, price = ?, available = ? WHERE id = ?",
        [input.name, input.price, input.available, Number(input.id)]
      );
      if (result.affectedRows === 0) {
        throw new GraphQLError(`No dish found with id ${input.id}`, {
          extensions: { code: "NOT_FOUND" },
        });
      }
      const [rows] = await pool.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [Number(input.id)]
      );
      return toDish(rows[0]);
    },
  },
};

const app = express();
const apollo = new ApolloServer({ typeDefs, resolvers });
const port = Number(process.env.PORT || 4000);

await testDatabaseConnection();
await apollo.start();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));
app.use("/graphql", expressMiddleware(apollo));

app.listen(port, () => {
  console.log(`CampusEats Assignment 7 is running at http://localhost:${port}`);
  console.log(`GraphQL endpoint: http://localhost:${port}/graphql`);
});

async function shutdown() {
  await apollo.stop();
  await pool.end();
  process.exit(0);
}
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
