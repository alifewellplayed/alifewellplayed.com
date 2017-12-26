<template>
    <div id="rep_home" class="container-fluid padding-10 sm-padding-10">
        <div class="row">
            <div class="col-md-8">

                <div class="row">
                    <div class="col-md-6">
                        <section class="panel panel-default replica-panel entry-donut-stats">
            				<div class="panel-header">
            					<h4 class="panel-title"><i class="fa fa-bar-chart-o"></i> My Stats</h4>
            				</div>
            				<div class="panel-body">
                                <dash-doughnut-entries :chart-data="site_stats_user" ></dash-doughnut-entries>
            				</div>
            			</section>
                    </div><!-- col-md-6 -->

                    <div class="col-md-6">
        				<section class="panel panel-default replica-panel entries">
        					<div class="panel-header">
        						<h4 class="panel-title"><i class="fa fa-check-square-o"></i> Scheduled Entries</h4>
        					</div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item" v-for="upcoming in upcoming_entries.results">{{upcoming.title}}</li>
                            </ul>
        				</section>

        				<section id="ideas" class="panel panel-default replica-panel entries">
        					<div class="panel-header">
        						<h4 class="panel-title"><i class="fa fa-pencil-square-o"></i> Ideas</h4>
        					</div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item ist-unstyled replica-list-item" v-for="idea in idea_entries.results">
                                    <router-link :to="{ name: 'EntryDetail', params: { entryID: idea.id }}" tag="h5" class="replica-clickable">{{idea.title}}</router-link>
                                    <div class="row">
                                        <div class="col-sm-4">
                                            <span class="wordcount">{{idea.total_words}} words</span>
                                        </div>
                                        <div class="col-sm-8 text-right">
                                            <span class="lastupdated">Updated: {{ idea.date_updated | moment("from") }}</span>
                                        </div>
                                    </div>
                                </li>
                            </ul>
        				</section>
        			</div><!-- scol-md-6 -->
                </div><!-- .row -->
            </div><!-- col-md-7 -->

            <div class="col-md-4">
                <section class="panel panel-default replica-panel">
        			<div class="panel-header">
        				<div class="pull-right"><a class="green" href="#"><i class="fa fa-plus-circle"></i></a></div>
        				<h4 class="panel-title"><i class="fa fa-code-fork" aria-hidden="true"></i> Channels ({{channels.count.total}})</h4>
        			</div>
        			<ul class="list-group list-group-flush">
                        <li class="list-group-item" v-for="channel in channels.results">{{channel.title}}</li>
                    </ul>
        		</section>

                <section class="panel panel-default replica-panel">
        			<div class="panel-header">
        				<div class="pull-right"><a class="green" href="#"><i class="fa fa-plus-circle"></i></a></div>
        				<h4 class="panel-title"><i class="fa fa-tags"></i> Topics ({{topics.count.total}})</h4>
        			</div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item" v-for="topic in topics.results">{{topic.title}}</li>
                    </ul>
        		</section>

        		<section class="panel panel-default replica-panel replica-media">
        			<div class="panel-header">
        				<div class="pull-right"><a class="green" href="#"><i class="fa fa-plus-circle"></i></a></div>
        				<h4 class="panel-title"><i class="fa fa-picture-o"></i> Media</h4>
        			</div>

        		</section>
            </div>
        </div><!-- .row -->
    </div>
</template>

<script>
    import DashDoughnutEntries from './components/DashDoughnutEntries.vue'

    var colors = [
        "#FF6384",
        "#36A2EB",
        "#FFCE56"
    ]

    var getColorArray = function (total) {
        var pool = [];
        for(var i=0; i<total; i++){
            pool.push(colors[i%colors.length]);
        }
        return pool;
    }

    var generateChartData = function(data){
        var labels = [];
        var values = [];
        $.each(data, function(key, value){
            labels.push(key);
            values.push(value);
        });
        var color_array = getColorArray(values.length);
        var results = {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: color_array,
            }]
        };
        return results;
    }

    export default {
        components: { DashDoughnutEntries, },
        data: function() {
            return {
                channels: {
                    results: [],
                    count: {
                        mine: 0,
                        total: 0,
                    },
                },
                topics: {
                    results: [],
                    count: {
                        mine: 0,
                        total: 0,
                    }
                },
                upcoming_entries: [],
                idea_entries: {
                    results: [],
                    count: {
                        mine: 0,
                        total: 0,
                    },
                },
                site_stats_global: {
                    channels: 0,
                    topics: 0
                },
                site_stats_user: generateChartData([]),
            }
        },
        created: function () {
            this.fetchData()
        },
        methods: {
            fetchData: function () {
                this.$http.get('/api/v2/dashboard/').then(function(data){
                    this.channels =  data.body.channels;
                    this.topics =  data.body.topics;
                    this.upcoming_entries =  data.body.upcoming_entries;
                    this.idea_entries =  data.body.ideas;
                    this.chart_data = {
                        upcoming: data.body.upcoming_entries.count.mine,
                        published: data.body.published_entries.count.mine,
                        ideas: data.body.ideas.count.mine,
                        pages: data.body.pages.count.mine
                    }
                    this.site_stats_user = generateChartData(this.chart_data);
                });
            }
        }
    }

</script>
