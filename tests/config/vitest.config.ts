import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const configDir = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(configDir, "..", "..");

export default {
  root: projectRoot,
  test: {
    include: ["tests/frontend/**/*.ts", "tests/frontend/**/*.tsx"],
    environment: "jsdom",
  },
};