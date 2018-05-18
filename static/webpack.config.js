const webpack = require('webpack');

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
        test: /\.(js|jsx)?$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: ['react']
            }
          }
        ],
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
    new MiniCssExtractPlugin('main.css')
  ],
  watch: true
};
module.exports = config;
