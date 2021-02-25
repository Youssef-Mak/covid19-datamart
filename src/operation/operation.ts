import { PoolClient } from "pg";
import { connectClient } from "../database";

/**
 * A generic operation performing some process.
 */
abstract class Operation<K extends object, T> {
  protected abstract perform(input: K): T;
}

/**
 * A generic asynchronous operation performing some process.
 */
abstract class OperationAsync<K extends object, T> {
  protected abstract async perform(input: K): Promise<T>;
}

/**
 * Base required input for any datastores operation.
 */
interface DatastoresOperationInput {
  client?: PoolClient;
}

/**
 * An operation involving datastores.
 * A client can be taken from the pool, or provided through input
 * if part of a transaction.
 * The client will be automatically setup and released when the operation is finished.
 * The client will only be released if connected on the fly.
 */
class DatastoresOperation<K extends DatastoresOperationInput, T> {
  private _client: PoolClient | undefined;
  private _shouldReleaseClient: boolean | undefined;

  protected get client() {
    return this._client as PoolClient;
  }

  /**
   * Transaction that is by default un-atomic
   * @param input Query input potentially providing a client
   */
  protected async doPerform(input: K) {
    let result: T | undefined;

    try {
      await this.setupQueries(input);
      result = await this.perform(input);
    } catch (e) {
      this.releaseClient();
      console.error(e);
      throw e;
    } finally {
      this.releaseClient();
    }

    return result;
  }

  /**
   * Method containing the 'meat' of the transaction(eg. new user insertion)
   * @param _input Query input potentially providing a client
   */
  protected async perform(_input: K): Promise<T> {
    throw new Error("You must override #perform.");
  }

  /**
   * Withholds client from pool or input
   * @param input Query input potentially providing a client
   */
  protected async setupQueries(input: K) {
    const { client: inputClient } = input;
    this._client = inputClient || (await connectClient());
    this._shouldReleaseClient = !inputClient;
  }

  /**
   * Releases client IFF client is borrowed(ie. provided from input)
   */
  protected releaseClient() {
    if (this._shouldReleaseClient) {
      try {
        this.client.release();
      } catch (err) {
        console.log("[PSQL] : Client already released");
      }
    }
  }
}

/**
 * A datastores operation that is wrapped in a transaction.
 * Optionally, #performWithoutTransaction can be used to avoid nested transactions.
 */
class AtomicDatastoresOperation<
  K extends DatastoresOperationInput,
  T
> extends DatastoresOperation<K, T> {
  /**
   * Administers operation atomically
   * @param input Query input potentially providing a client
   */
  protected async doPerform(input: K) {
    let result: T | undefined;

    try {
      await this.setupQueries(input);

      await this.begin();
      result = await this.perform(input);
      await this.commit();
    } catch (e) {
      this.rollback();
      this.releaseClient();
      console.error(e);
      throw e;
    } finally {
      this.releaseClient();
    }

    return result;
  }

  /**
   * Indicate beginning of sequence
   */
  protected async begin() {
    await this.client.query<never>("BEGIN");
  }

  /**
   * Store changes performed by transaction
   */
  protected async commit() {
    await this.client.query<never>("COMMIT");
  }

  /**
   * Revert changes performed by transaction
   */
  protected async rollback() {
    await this.client.query<never>("ROLLBACK");
  }
}

export {
  Operation,
  OperationAsync,
  DatastoresOperation,
  AtomicDatastoresOperation,
  DatastoresOperationInput,
};
