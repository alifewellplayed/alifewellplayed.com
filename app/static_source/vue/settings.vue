<template>
    <div id="rep_entries" class="container-fluid">
        <div class="row">
            <div class="col-md-4">
                <section class="card card-default replica-card">
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">All Posts</li>
                        <li class="list-group-item">Published</li>
                        <li class="list-group-item">Upcoming</li>
                        <li class="list-group-item">Ideas (drafts)</li>
                    </ul>
                </section>
                <section id="replica-new-idea" class="card card-default replica-card">
                    <div class="card-header">
                        <h4 class="card-title">Sort by Topic</h4>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item" v-for="topic in topics">{{topic.title}}</li>
                    </ul>
                </section>
            </div>
            <div class="col-md-8">
                <section class="card card-default replica-card">
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item" v-for="entry in entries">{{entry.title}}</li>
                    </ul>
                </section>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data: function() {
            return {
                SiteSettings: [],
            }
        },
        created: function () {
            this.fetchData()
        },
        methods: {
            fetchData: function () {
                this.$http.get('/api/v2/current/settings').then(function(data){
                    this.SiteSettings =  data.body;
                });
            }
        }
    }
</script>
