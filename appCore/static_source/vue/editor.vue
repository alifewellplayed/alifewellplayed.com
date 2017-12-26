<template>
    <div id="editor" class="container-fluid">
        <div class="row">
            <div class="col-md-12">
                <div class="card card-default replica-card">
                    <input type="text" name="post-title" class="form-control" placeholder="Title" v-model="title" />
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <textarea class="form-control" :value="input" @input="update" name="post-content"></textarea>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-block">
                        <div v-html="compiledMarkdown"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <button class="btn btn-primary" v-on:click="save">Save Post</button>
        </div>
    </div>
</template>

<script>
var marked = require('marked');
var _ = require('lodash');

var entry_api_url = "/api/v2/entries/new/";
export default {
    data: function(){
        return {
            input: '# hello',
            post_id: null,
            title: '',
        }
    },
    computed: {
        compiledMarkdown: function () {
            return marked(this.input, { sanitize: true })
        },
        slug: function(){
            return this.title.toLowerCase()
                .replace(/[^\w ]+/g,'')
                .replace(/ +/g,'-');
        }
    },
    methods: {
        update: _.debounce(function (e) {
            this.input = e.target.value
        }, 300),
        save: function(event){
            // Save the post
            var post_obj = {
                title: this.title,
                slug: this.slug,
                content_format: "markdown",
                body: this.input,
                body_html: this.compiledMarkdown,
            };
            // do the POST
            console.log(post_obj);
            console.log("Posting data.");
            this.$http.post(entry_api_url, post_obj, {credentials: true}).then(function(data){
                // Post successful
                console.log("post successful");
                console.log(data);
            },
            function(data){
                // Post failed
                console.log('post failed');
                console.log(data);
            });
        }
    }
}
</script>
