import dotenv from "dotenv";

let ENVIRONMENT_SERVICE_INSTANCE: EnvironmentService;

type EnvironmentVariables = {
  PGHOST: string;
  PGUSER: string;
  PGPASSWORD: string;
  PGDATABASE: string;
  PGPORT: string;
};

class EnvironmentService {
  private config: dotenv.DotenvConfigOutput;

  constructor() {
    this.config = dotenv.config({
      path: `${__dirname}/.env`,
    });
    if (!this.config || this.config.error || !this.config.parsed) {
      console.error("Error: failed to load environment variables");
      console.error(this.config.error);
      process.exit(1);
    }
  }

  public get variables() {
    return this.config.parsed as EnvironmentVariables;
  }
}

function EnvironmentServiceInstance() {
  if (!ENVIRONMENT_SERVICE_INSTANCE) {
    ENVIRONMENT_SERVICE_INSTANCE = new EnvironmentService();
  }
  return ENVIRONMENT_SERVICE_INSTANCE;
}

export { EnvironmentServiceInstance };
