// Webpack dev server
import webpack from 'webpack';
import WebpackDevServer from 'webpack-dev-server';

import config from './webpack.config';
// This is a "custom" config I took from another project 
// because I was having issues with the more complex
// config that came with the boilerplate. If you experience
// issues, consider looking at `webpack.base.config.js`
// and `webpack.local.config.js`

new WebpackDevServer(webpack(config), {
  compress: true,
  public: 'aggieisb.com',
  publicPath: config.output.publicPath,
  port: 3000,
  hot: true, // reload webpack every time it detects changes, not working for some reason
  inline: true,
  historyApiFallback: true,
  proxy: {
    '/api/*': {
      target: 'http://0.0.0.0:8000/',
      secure: 'false',
    },
    '/rest-auth/*': {
      target: 'http://0.0.0.0:8000/',
      secure: 'false',
    },
  },
  headers: { 'Access-Control-Allow-Origin': '*' },
}).listen(3000, '0.0.0.0', (err) => {
  if (err) {
    console.log(err);
  }

  console.log('Listening at 0.0.0.0:3000');
});
