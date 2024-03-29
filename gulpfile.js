/*!
 * Based on UnderTasker
 * Copyright 2018 Tyler Rilling
 * Licensed under MIT (https://github.com/underlost/Undertasker/blob/master/LICENSE)
 */

// grab our packages
var gulp = require('gulp'),
    webpack = require('webpack-stream');
    jshint = require('gulp-jshint');
    sass = require('gulp-sass');
    sourcemaps = require('gulp-sourcemaps');
    concat = require('gulp-concat');
    autoprefixer = require('gulp-autoprefixer');
    cleanCSS = require('gulp-clean-css');
    rename = require('gulp-rename'); // to rename any file
    uglify = require('gulp-uglify');
    del = require('del');
    stylish = require('jshint-stylish');
    runSequence = require('run-sequence');
    coffee = require('gulp-coffee');
    gutil = require('gulp-util');
    imagemin = require('gulp-imagemin');
    git = require('gulp-deploy-git');
    gulpWebpack = require('webpack-stream');

// Cleans the web dist folder
gulp.task('clean', function () {
  return del([
    'dist/',
    'appCore/static/site',
    'appCore/static/admin',
    'appCore/**/*.pyc'
  ]);
});

// Clear cache
gulp.task('clean-cache', function () {
  del(['appCore/**/*.pyc']);
});

gulp.task('copy-dist', function() {
  gulp.src('dist/**/*.*')
  .pipe(gulp.dest('appCore/static'));
});

// Copy fonts task
gulp.task('copy-fonts', function() {
  gulp.src('appCore/static_source/fonts/site/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/site/fonts'));
  gulp.src('node_modules/components-font-awesome/webfonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/site/fonts'));
});
gulp.task('admin-fonts', function() {
  gulp.src('appCore/static_source/fonts/admin/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/admin/fonts'));
  gulp.src('node_modules/components-font-awesome/webfonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
  .pipe(gulp.dest('dist/admin/fonts'));
});

// Minify Images
gulp.task('imagemin', function() {
  return gulp.src('appCore/static_source/img/site/**/*.{jpg,png,gif,ico}')
  .pipe(imagemin())
  .pipe(gulp.dest('dist/site/img'))
});
gulp.task('admin-imagemin', function() {
  return gulp.src('appCore/static_source/img/admin/**/*.{jpg,png,gif,ico}')
  .pipe(imagemin())
  .pipe(gulp.dest('dist/admin/img'))
});

// Copy component assets
gulp.task('install', function() {
  gulp.src('node_modules/components-font-awesome/scss/**/*.*')
  .pipe(gulp.dest('appCore/static_source/sass/_shared/font-awesome'));

  gulp.src('node_modules/bootstrap/scss/**/*.*')
  .pipe(gulp.dest('appCore/static_source/sass/_shared/bootstrap'));
});

// Compile coffeescript to JS
gulp.task('brew-coffee', function() {
  return gulp.src('appCore/static_source/coffee/*.coffee')
  .pipe(coffee({bare: true}).on('error', gutil.log))
  .pipe(gulp.dest('appCore/static_source/js/coffee/'))
});

// CSS Build Task for main site/theme
gulp.task('build-css', function() {
  return gulp.src('appCore/static_source/sass/site.scss')
  .pipe(sass().on('error', sass.logError))
  .pipe(autoprefixer({
    browsers: ['last 2 versions'],
    cascade: false
  }))
  .pipe(gulp.dest('dist/site/css'))
  .pipe(cleanCSS())
  .pipe(rename('site.min.css'))
  .pipe(gulp.dest('dist/site/css'))
  .on('error', sass.logError)
});

// CSS Build Task for Dashboard
gulp.task('admin-build-css', function() {
  return gulp.src('appCore/static_source/sass/admin.scss')
  .pipe(sass().on('error', sass.logError))
  .pipe(autoprefixer({
    browsers: ['last 2 versions'],
    cascade: false
  }))
  .pipe(gulp.dest('dist/admin/css'))
  .pipe(cleanCSS())
  .pipe(rename('admin.min.css'))
  .pipe(gulp.dest('dist/admin/css'))
  .on('error', sass.logError)
});

// Concat All JS into unminified single file
gulp.task('concat-js', function() {
  return gulp.src([
    'node_modules/jquery/dist/jquery.js',
    'node_modules/popper.js/dist/umd/popper.min.js',
    'node_modules/fullpage.js/dist/jquery.fullpage.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/jquery.easing/js/jquery.easing.js',
    //'node_modules/animejs/anime.js',
    'node_modules/pace-progress/pace.js',
    'appCore/static_source/js/site/vline.jquery.js',
    'appCore/static_source/js/site/site.js',
    'appCore/static_source/js/coffee/*.*',
  ])
  .pipe(sourcemaps.init())
  .pipe(concat('site.js'))
  .pipe(sourcemaps.write('./maps'))
  .pipe(gulp.dest('dist/site/js'));
});

//gulp.task('admin-webpack-vue', function(){
//    return gulp.src('appCore/static_source/js/admin/app.js')
//        .pipe(gulpWebpack(require('./webpack.config.js'), webpack))
//        .pipe(gulp.dest('dist/admin/js'));
//});

gulp.task('admin-webpack-vue', function() {
  return gulp.src('appCore/static_source/js/admin/app.js')
  .pipe(webpack( require('./webpack.config.js') ))
  .pipe(gulp.dest('dist/admin/js'));
});

// Concat admin JS into unminified single file
gulp.task('admin-concat-js', function() {
  return gulp.src([
    'node_modules/jquery/dist/jquery.js',
    'node_modules/popper.js/dist/umd/popper.min.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/simplemde/dist/simplemde.min.js',
    'node_modules/autosize/dist/autosize.js',
    'node_modules/pace-progress/pace.js',
    'appCore/static_source/js/admin/jquery.appear.js',
    'node_modules/bootstrap-datepicker/js/bootstrap-datepicker.js',
    'node_modules/timepicker/jquery.timepicker.js',
    'appCore/static_source/js/admin/clipboard.js',
    'appCore/static_source/js/admin/site.js',
  ])
  .pipe(sourcemaps.init())
  .pipe(concat('global.js'))
  .pipe(sourcemaps.write('./maps'))
  .pipe(gulp.dest('dist/admin/js'));
});

// Concat codemirror HTML editor files
gulp.task('concat-codemirror', function() {
  return gulp.src([
    'node_modules/codemirror/lib/codemirror.js',
    'node_modules/codemirror/addon/selection/selection-pointer.js',
    'node_modules/codemirror/mode/xml/xml.js',
    'node_modules/codemirror/mode/css/css.js',
    'node_modules/codemirror/mode/javascript/javascript.js',
    'node_modules/codemirror/mode/vbscript/vbscript.js',
    'node_modules/codemirror/mode/htmlmixed/htmlmixed.js',
  ])
  .pipe(sourcemaps.init())
  .pipe(concat('codemirror.js'))
  .pipe(sourcemaps.write('./maps'))
  .pipe(gulp.dest('dist/admin/js'));
});

// configure the jshint task
gulp.task('jshint', function() {
  return gulp.src('appCore/static_source/js/site/*.js')
  .pipe(jshint())
  .pipe(jshint.reporter('jshint-stylish'));
});

// jshint admin task
gulp.task('admin-jshint', function() {
  return gulp.src('appCore/static_source/js/admin/*.js')
  .pipe(jshint())
  .pipe(jshint.reporter('jshint-stylish'));
});

// Shrinks all the site js
gulp.task('shrink-js', function() {
  return gulp.src('dist/site/js/site.js')
  .pipe(uglify())
  .pipe(rename('site.min.js'))
  .pipe(gulp.dest('dist/site/js'))
});

// Shrinks admin js
gulp.task('admin-shrink-js', function() {
  return gulp.src('dist/admin/js/global.js')
  .pipe(uglify())
  .pipe(rename('global.min.js'))
  .pipe(gulp.dest('dist/admin/js'))
});

// Javascript build task for frontend
gulp.task('build-js', function(callback) {
  runSequence('concat-js', 'shrink-js', callback);
});

// Javascript build task for admin
gulp.task('admin-build-js', function(callback) {
  runSequence('admin-webpack-vue', 'admin-concat-js', 'admin-shrink-js', 'concat-codemirror', callback);
  // 'admin-shrink-js'
});

// configure which files to watch and what tasks to use on file changes
gulp.task('watch', function() {
  gulp.watch('appCore/static_source/coffee/**/*.js', ['brew-coffee', 'copy-dist']);
  gulp.watch('appCore/static_source/js/**/*.js', ['build-js', 'admin-build-js', 'copy-dist']);
  gulp.watch('appCore/static_source/vue/**/*.vue', ['admin-build-js', 'copy-dist']);
  gulp.watch('appCore/static_source/sass/**/*.scss', ['build-css', 'admin-build-css', 'copy-dist' ] );
});

// Build task for admin
gulp.task('admin', function(callback) {
  runSequence(
    ['admin-build-css', 'admin-build-js'],
    'admin-imagemin', 'copy-dist', callback
  );
});

// Build task for theme/frontend
gulp.task('build', function(callback) {
  runSequence(
    ['build-css', 'build-js'],
    'imagemin', 'copy-dist', callback
  );
});

// Default task will build both assets.
gulp.task('default', ['build', 'admin']);
