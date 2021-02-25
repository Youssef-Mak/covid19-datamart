import { AtomicDatastoresOperation } from "../../operation/operation";

/**
 * Maintenance operations are self contained, atomic datastores operations.
 * No input should be needed, and no output will be given.
 * Maintenance operations should be timing agnostic. That means that
 * a maintenance operation run at any time in the future should still produce a correct result.
 * They should also be able to be run several times without any unwanted side effects.
 */
class MaintenanceTask extends AtomicDatastoresOperation<any, void> {
  protected async doPerform() {
    const input = {};

    try {
      await this.setupQueries(input);

      await this.begin();
      await this.perform();
      await this.commit();
    } catch (e) {
      this.rollback();
      this.releaseClient();
      console.error(e);
      throw e;
    } finally {
      this.releaseClient();
    }
  }

  protected async perform() {
    throw new Error("You must override #perform.");
  }
}

export { MaintenanceTask };
