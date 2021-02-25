import pg from "pg";
import { EnvironmentServiceInstance } from "../services/environment-service";

// tslint:disable-next-line:no-var-requires
const pgCamelCase = require("pg-camelcase");
pgCamelCase.inject(pg);

const config = EnvironmentServiceInstance().variables;

const pool = new pg.Pool({
  host: config.PGHOST,
  user: config.PGUSER,
  password: config.PGPASSWORD,
  database: config.PGDATABASE,
  port: +config.PGPORT,
});

async function connectClient() {
  return await pool.connect();
}

export { connectClient };
