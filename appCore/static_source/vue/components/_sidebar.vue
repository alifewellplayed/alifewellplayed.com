<template>
    <div>
        <div class="sidebar-header">
            <router-link :to="{ name: 'Home' }" tag="img" src="/static/admin/img/replica_logo.png" alt="logo" class="brand replica-clickable" data-src="/static/admin/img/replica_logo.png" data-src-retina="/static/admin/img/replica_logo.png" width="22" height="22" />
            <div class="sidebar-header-controls pull-right">
                <button type="button" class="btn btn-link visible-lg-inline" data-toggle-pin="sidebar"><i class="fa fs-12"></i>
                </button>
            </div>
        </div>
        <div class="scroll-wrapper menu-items">
            <ul class="menu-items">
                <li class="m-t-30">
                    <router-link :to="{ name: 'Home' }" class="detailed">
                        <span class="title">Dashboard</span>
                        <span class="details">User Metrics</span>
                    </router-link>
                    <router-link :to="{ name: 'Home' }" class="bg-success icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-home" aria-hidden="true"></i>
                    </router-link>
                </li>
                <li class="">
                    <router-link :to="{ name: 'EntryList' }" class="detailed">
                        <span class="title">Posts</span>
                        <span class="details">{{total_counts.published}} items</span>
                    </router-link>
                    <router-link :to="{ name: 'EntryList' }" class="icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
                    </router-link>
                </li>
                <li class="">
                    <router-link :to="{name:'NotesHome'}" class="detailed">
                        <span class="title">Notes</span>
                        <span class="details">{{total_counts.notes}} items</span>
                    </router-link>
                    <router-link :to="{name:'NotesHome'}" class="icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-book" aria-hidden="true"></i>
                    </router-link>
                </li>

                <li class="">
                    <router-link :to="{name:'TopicList'}" class="detailed">
                        <span class="title">Topics</span>
                        <span class="details">{{total_counts.topics}} items</span>
                    </router-link>
                    <router-link :to="{name:'TopicList'}" class="icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-tags" aria-hidden="true"></i>
                    </router-link>
                </li>
                <li class="">
                    <router-link :to="{name:'ChannelList'}"  class="detailed">
                        <span class="title">Channels</span>
                        <span class="details">{{total_counts.channels}} items</span>
                    </router-link>
                    <router-link :to="{name:'ChannelList'}" class="icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-code-fork" aria-hidden="true"></i>
                    </router-link>
                </li>
                <li class="">
                    <router-link :to="{name:'MediaList'}"  class="detailed">
                        <span class="title">Media</span>
                        <span class="details">{{total_counts.media}} items</span>
                    </router-link>
                    <router-link :to="{name:'MediaList'}" class="icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-file-image-o" aria-hidden="true"></i>
                    </router-link>
                </li>
                <li class="">
                    <router-link :to="{name:'SiteSettings'}"  class="detailed">
                        <span class="title">Settings</span>
                        <span class="details">Site controls</span>
                    </router-link>
                    <router-link :to="{name:'SiteSettings'}" class="icon-thumbnail replica-clickable" tag="span">
                        <i class="fa fa-cogs" aria-hidden="true"></i>
                    </router-link>
                </li>

            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        data: function () {
            return {
                total_counts: {},
                user_counts: {},
            }
        },
        created: function () {
            this.fetchData()
        },

        ready: function(){
            this.init();
        },
        methods: {
            init() {
                this.fetchData();
            },
            fetchData: function () {
                this.$http.get('/api/v2/current/stats/').then(function(data){
                    this.total_counts = data.body.total_counts;
                    this.user_counts = data.body.user_counts;
                });

            }
        }
    }
</script>
