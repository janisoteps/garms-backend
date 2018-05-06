const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const config = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader"
        ]
      },
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
          test: /\.(png|svg|jpg|gif)$/,
          use: 'file-loader'
      }
    ]
  },
  entry:  __dirname + '/js/index.jsx',
  output: {
      path: __dirname + '/dist',
      filename: 'bundle.js',
  },
  resolve: {
      extensions: ['.js', '.jsx', '.css']
  },
  plugins: [
    new MiniCssExtractPlugin('main.css'),
    new UglifyJSPlugin()
  ]
};
module.exports = config;
