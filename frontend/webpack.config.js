const path = require("path");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "main.js",
  },
  mode: "development",
  devServer: {
    static: path.join(__dirname, "public"),
    port: 3000,
    host: "0.0.0.0",
  },
};

