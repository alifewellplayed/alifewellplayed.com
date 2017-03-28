var vue = require('vue-loader')
var webpack = require("webpack")

module.exports = {
    entry: [
        './app/static_source/js/admin/app.js'
    ],
    output: {
        path: "/dist/js",
        publicPath: "/dist/",
        filename: "app.js"
    },
    module: {
        loaders: [
            {
                test: /\.vue$/,
                loader: 'vue'
            },
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel'
            },
        ]
    },
    babel: {
        presets: ['es2015'],
        plugins: ['transform-runtime']
    }
}
