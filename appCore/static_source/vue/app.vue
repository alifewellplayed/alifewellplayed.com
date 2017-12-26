<template>
    <div class="replica-container">
        <nav class="page-sidebar" data-pages="sidebar">
            <site-sidebar class="sidebar-menu" id="appMenu"></site-sidebar>
        </nav>
        <div class="page-container ">
            <header class="header navbar navbar-default">
                <div class="container-fluid">

                    <div class="collapse navbar-collapse" id="site-header">
                        <ul class="nav navbar-nav">
                            <li class="dropdown">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                                    <i class="fa fa-home fa-lg" aria-hidden="true"></i>
                                </a>
                                <ul class="dropdown-menu">
                                    <li><router-link class="dropdown-item" to="/">Home</router-link></li>
                                    <li><a class="dropdown-item" v-bind:href="site_settings.site_url">View Site</a></li>
                                </ul>
                            </li>
                            <li class="dropdown">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dashboard <span class="caret"></span></a>
                                <ul class="dropdown-menu">
                                    <li><router-link to="/entries">Posts</router-link></li>
                                    <li><router-link to="/pages">Pages</router-link></li>
                                    <li><router-link to="/notes">Notes</router-link></li>
                                    <li><router-link to="/topics">Topics</router-link></li>
                                    <li><router-link to="/channels">Channels</router-link></li>
                                    <li><router-link to="/media">Media</router-link></li>
                                </ul>
                            </li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li class="dropdown">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                                    {{user_settings.current_user}}
                                    <img class="img-circle" id="avatar" width="24" height="24" v-bind:src="user_settings.current_avatar" />
                                </a>
                                <ul class="dropdown-menu">
                                    <li><a v-bind:href="user_settings.AccountSettings">Account Settings</a></li>
                                    <li><a v-bind:href="user_settings.password_change">Change Password</a></li>
                                    <li role="separator" class="divider"></li>
                                    <li><a v-bind:href="user_settings.logout">Logout</a></li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
            </header>

            <div class="page-content-wrapper ">
                <div class="content">
                    <router-view class="site-content" transition="fadein"></router-view>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // import SiteHeader from './components/_header.vue';
    import SiteSidebar from './components/_sidebar.vue';
    import SiteFooter from './components/_footer.vue';
    export default {
        replace: false,
        components: {
            //SiteHeader,
            SiteSidebar,
            SiteFooter
        },
        data: function () {
            return {
                parentMsg: 'test',
                site_settings: {},
                user_settings: {},
            };
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
                this.$http.get('/api/v2/current/').then(function(data){
                    this.site_settings = data.body.site_settings;
                    this.user_settings = data.body.user_settings;
                });

            }
        }
    }
</script>
