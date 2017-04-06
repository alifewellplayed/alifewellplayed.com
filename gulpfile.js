/*!
 * Based on UnderTasker
 * Copyright 2017 Tyler Rilling
 * Licensed under MIT (https://github.com/underlost/Undertasker/blob/master/LICENSE)
 */

// grab our packages
var gulp   = require('gulp'),
    child = require('child_process');
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
    bower = require('gulp-bower');
    imagemin = require('gulp-imagemin');
    git = require('gulp-deploy-git');
    browserSync = require('browser-sync');
    $ = require('gulp-load-plugins')();
    babel = require('gulp-babel');
    webpack = require('webpack-stream');

// Cleans the web dist folder
gulp.task('clean', function () {
    return del([
        'dist/',
        'app/static/site',
        'app/static/admin',
        'app/**/*.pyc'
    ]);
});

// Clear cache
gulp.task('clean-cache', function () {
    del(['app/**/*.pyc']);
});

gulp.task('copy-dist', function() {
    gulp.src('dist/**/*.*')
    .pipe(gulp.dest('app/static'));
});

// Copy fonts task
gulp.task('copy-fonts', function() {
    gulp.src('app/static_source/fonts/site/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
    .pipe(gulp.dest('dist/site/fonts'));
    gulp.src('bower_components/components-font-awesome/fonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
    .pipe(gulp.dest('dist/site/fonts'));
});
gulp.task('admin-fonts', function() {
    gulp.src('app/static_source/fonts/admin/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
    .pipe(gulp.dest('dist/admin/fonts'));
    gulp.src('bower_components/components-font-awesome/fonts/**/*.{ttf,woff,eof,svg,eot,woff2,otf}')
    .pipe(gulp.dest('dist/admin/fonts'));
});

// Minify Images
gulp.task('imagemin', function() {
    return gulp.src('app/static_source/img/site/**/*.{jpg,png,gif,ico}')
	.pipe(imagemin())
	.pipe(gulp.dest('dist/site/img'))
});
gulp.task('admin-imagemin', function() {
    return gulp.src('app/static_source/img/admin/**/*.{jpg,png,gif,ico}')
	.pipe(imagemin())
	.pipe(gulp.dest('dist/admin/img'))
});

// Copy Bower components
gulp.task('copy-bower', function() {
    gulp.src('bower_components/components-font-awesome/scss/**/*.*')
    .pipe(gulp.dest('app/static_source/sass/font-awesome'));

    gulp.src('bower_components/bootstrap-sass/assets/stylesheets/**/*.*')
    .pipe(gulp.dest('app/static_source/sass/bootstrap'));
});

// Runs Bower update
gulp.task('bower-update', function() {
    return bower({ cmd: 'update'});
});

// Bower tasks
gulp.task('bower', function(callback) {
    runSequence(
        'bower-update', 'copy-bower', callback
    );
});

// Compile coffeescript to JS
gulp.task('brew-coffee', function() {
    return gulp.src('app/static_source/coffee/*.coffee')
        .pipe(coffee({bare: true}).on('error', gutil.log))
        .pipe(gulp.dest('app/static_source/js/coffee/'))
});

// CSS Build Task for main site/theme
gulp.task('build-css', function() {
  return gulp.src('app/static_source/sass/site.scss')
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
  return gulp.src('app/static_source/sass/admin.scss')
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
        'bower_components/jquery/dist/jquery.js',
        'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
        'bower_components/jquery.easing/js/jquery.easing.js',
        'app/static_source/js/lib/jquery.appear.js',
        'bower_components/PACE/pace.js',
        'app/static_source/js/site/site.js',
        'app/static_source/js/coffee/*.*',
    ])
    .pipe(sourcemaps.init())
        .pipe(concat('global.js'))
        .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest('dist/site/js'));
});

gulp.task('admin-webpack-vue', function(){
    return gulp.src('app/static_source/js/admin/app.js')
        .pipe(webpack(require('./webpack.config.js')))
        .pipe(gulp.dest('dist/admin/js'));
});

// Concat admin JS into unminified single file
gulp.task('admin-concat-js', function() {
    return gulp.src([
        'app/static_source/js/admin/modernizr.custom.js',
        'bower_components/jquery/dist/jquery.js',
        'bower_components/tether/dist/js/tether.js',
        'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
        'bower_components/PACE/pace.js',
        //'bower_components/jquery-ui/jquery-ui.min.js',
        //'bower_components/jquery-bez/jquery.bez.min.js',
        //'bower_components/select2/dist/js/select2.js',
        //'bower_components/jquery.scrollbar/jquery.scrollbar.js',
        //'bower_components/jquery-unveil/jquery.unveil.js',
        //'bower_components/jquery.actual/jquery.actual.min.js',
        //'app/static_source/js/admin/jquery-easy.js',
        //'bower_components/switchery/dist/switchery.js',
        //'bower_components/classie/classie.js',
        //'bower_components/metrojs/release/MetroJs.Full/MetroJs.min.js',
        'app/static_source/js/admin/jquery.appear.js',
        //'app/static_source/js/admin/pages.js',
        'app/static_source/js/admin/site.js',
    ])
    .pipe(sourcemaps.init())
        .pipe(concat('global.js'))
        .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest('dist/admin/js'));
});

// configure the jshint task
gulp.task('jshint', function() {
    return gulp.src('app/static_source/js/site/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish'));
});

// jshint admin task
gulp.task('admin-jshint', function() {
    return gulp.src('app/static_source/js/admin/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish'));
});

// Shrinks all the site js
gulp.task('shrink-js', function() {
    return gulp.src('dist/js/site/global.js')
    .pipe(uglify())
    .pipe(rename('site.min.js'))
    .pipe(gulp.dest('dist/js/site'))
});

// Shrinks all the admin js
gulp.task('admin-shrink-js', function() {
    return gulp.src('dist/admin/js/*.js')
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
    runSequence('admin-webpack-vue', 'admin-concat-js', callback);
    // 'admin-shrink-js'
});

// configure which files to watch and what tasks to use on file changes
gulp.task('watch', function() {
    gulp.watch('app/static_source/coffee/**/*.js', ['brew-coffee', 'copy-dist']);
    gulp.watch('app/static_source/js/**/*.js', ['build-js', 'admin-build-js', 'copy-dist']);
    gulp.watch('app/static_source/vue/**/*.vue', ['admin-build-js', 'copy-dist']);
    gulp.watch('app/static_source/sass/**/*.scss', ['build-css', 'admin-build-css', 'copy-dist' ] );
});

// Default build task
gulp.task('build-admin', function(callback) {
    runSequence(
        ['admin-build-css', 'admin-build-js'],
        'admin-imagemin', 'copy-dist', callback
    );
});

// Default build task
gulp.task('build-site', function(callback) {
    runSequence(
        ['build-css', 'build-js'],
        'imagemin', 'copy-dist', callback
    );
});

// Build All
gulp.task('build', function(callback) {
    runSequence(
        ['build-admin'], ['build-site'], callback
    );
});

// Default task will build the assets then watch for any updates to files.
gulp.task('default', ['build', 'watch']);
