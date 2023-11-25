import * as path from 'path';
// eslint-disable-next-line @nrwl/nx/enforce-module-boundaries
import { FastifyInstance } from 'fastify';
// eslint-disable-next-line @nrwl/nx/enforce-module-boundaries
import AutoLoad from '@fastify/autoload';
// eslint-disable-next-line @nrwl/nx/enforce-module-boundaries
import fastifyMultipart from '@fastify/multipart';

/* eslint-disable-next-line */
export interface AppOptions {}

export async function app(fastify: FastifyInstance, opts: AppOptions) {
  fastify.register(fastifyMultipart);

  // Place here your custom code!

  // Do not touch the following lines

  // This loads all plugins defined in plugins
  // those should be support plugins that are reused
  // through your application
  fastify.register(AutoLoad, {
    dir: path.join(__dirname, 'plugins'),
    options: { ...opts },
  });

  // This loads all plugins defined in routes
  // define your routes in one of these
  fastify.register(AutoLoad, {
    dir: path.join(__dirname, 'routes'),
    options: { ...opts },
  });
}
