<template>
    <div id="rep_pages" class="container-fluid padding-10 sm-padding-10">
        <div class="row">
            <div class="col-md-12">

                <section class="panel panel-default replica-panel ">
                    <div class="panel-header">
                        <h4 class="panel-title"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> Pages</h4>
                    </div>
                    <div class="panel-body">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Title</th>
                                    <th>URL</th>
                                    <th>Updated</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="page in pages">
                                    <td scope="row">{{page.title}}</td>
                                    <td><span class="badge badge-default">{{page.url}}</span></td>
                                    <td>{{page.pub_date}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

            </div>
        </div>
    </div>
</template>


<script>
    export default {
        components: { },
        data: function() {
            return {
                pages: [],
            }
        },
        created: function () {
            this.fetchData()
        },
        methods: {
            fetchData: function () {
                this.$http.get('/api/v2/pages/').then(function(data){
                    this.pages =  data.body;
                });
            }
        }
    }
</script>
