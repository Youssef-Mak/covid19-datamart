import fs from "fs";
import path from "path";
import { MaintenanceTask } from "../maintenance-task";

/**
 * Runs the `create_datamart.sql` file.
 */
class CreateDatamart extends MaintenanceTask {
  public static async perform() {
    return new CreateDatamart().doPerform();
  }

  protected async perform() {
    const datamartPath = path.join(__dirname, "..", "..", "create_datamart.sql");
    const datamartFile = fs.readFileSync(datamartPath, "utf-8");

    try {
      await this.client.query<never>(datamartFile);
    } catch (error) {
      console.log(`Error while running CreateDatamart. ${error}`);
    }
  }
}

export default CreateDatamart;
