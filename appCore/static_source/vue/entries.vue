<template>
    <div id="rep_entries" class="container-fluid padding-10 sm-padding-10">
        <div class="row">
            <div class="col-md-4">
                <section class="panel panel-default replica-panel ">
                    <div class="panel-header">
                        <h4 class="panel-title"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> Entry Status</h4>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Published</li>
                        <li class="list-group-item">Upcoming</li>
                        <li class="list-group-item">Ideas (drafts)</li>
                    </ul>
                </section>
                <section id="replica-new-idea" class="panel panel-default replica-panel">
                    <div class="panel-header">
                        <h4 class="panel-title"><i class="fa fa-tags" aria-hidden="true"></i> Sort by Topic</h4>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item" v-for="topic in topics">{{topic.title}}</li>
                    </ul>
                </section>
            </div>
            <div class="col-md-8">
                <section class="panel panel-default replica-panel">
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
                topics: [],
                entries: [],
            }
        },
        created: function () {
            this.fetchData()
        },
        methods: {
            fetchData: function () {
                this.$http.get('/api/v2/topics/').then(function(data){
                    this.topics =  data.body;
                });
                this.$http.get('/api/v2/entries/').then(function(data){
                    this.entries =  data.body;
                });
            }
        }
    }
</script>
