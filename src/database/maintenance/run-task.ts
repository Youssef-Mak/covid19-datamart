import path from "path";
import _ from "lodash";
import { MaintenanceTask } from "./maintenance-task";

(async () => {
  if (process.argv.length !== 3) {
    console.error("Usage: yarn run maintenance <task>");
    process.exit(1);
  }

  const taskNameOriginal = process.argv[2];
  const taskName = _.upperFirst(_.camelCase(taskNameOriginal));

  const taskPath = path.join(__dirname, "tasks", taskNameOriginal);

  const taskImport = await import(taskPath).catch((_e) => {
    console.error(`Task ${taskName} not found.`);
    process.exit(1);
  });

  if (!taskImport?.default) {
    console.error(`Module ${taskName}.ts does not have a default export.`);
    process.exit(1);
  }

  const task = taskImport.default;

  if (!(task.prototype instanceof MaintenanceTask)) {
    console.error(`Task ${taskName} is not a MaintenanceTask.`);
    process.exit(1);
  }

  console.log(`Running ${taskName}.perform`);

  await task.perform();

  console.log("Wrapping up...");
})();
