<template>
<header class="header navbar navbar-toggleable-md">
    <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav mr-auto">
            <li class="nav-item dropdown">
                <router-link class="nav-link dropdown-toggle" to="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dashboard</router-link>
                <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                    <router-link class="dropdown-item" to="/">Home</router-link>
                    <a class="dropdown-item" v-bind:href="site_settings.site_url">View Site</a>
                    <router-link class="dropdown-item" to="/entries">Posts</router-link>
                    <router-link class="dropdown-item" to="/pages">Pages</router-link>
                    <router-link class="dropdown-item" to="/notes">Notes</router-link>
                    <router-link class="dropdown-item" to="/topics">Topics</router-link>
                    <router-link class="dropdown-item" to="/channels">Channels</router-link>
                    <router-link class="dropdown-item" to="/media">Media</router-link>
                </div>
            </li>

            <li class="nav-item">
                <router-link class="nav-link" to="/entries">Posts</router-link>
            </li>

            <li class="nav-item">
                <router-link class="nav-link" to="/pages">Pages</router-link>
            </li>

            <li class="nav-item">
                <router-link class="nav-link" to="/editor"><i class="fa fa-plus"></i> New</router-link>
            </li>

        </ul>
        <ul class="navbar-nav my-2 my-lg-0">
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">{{user_settings.current_user}}</a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                    <a class="dropdown-item" v-bind:href="user_settings.AccountSettings">Account Settings</a>
                    <a class="dropdown-item" v-bind:href="user_settings.password_change">Change Password</a>
                    <a class="dropdown-item" v-bind:href="user_settings.logout">Logout</a>
                </div>
            </li>
        </ul>
    </div>
</header>
</template>

<script>

    export default {

        data: function () {
            return {
                site_settings: {},
                user_settings: {},
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
                this.$http.get('/api/v2/current/').then(function(data){
                    this.site_settings = data.body.site_settings;
                    this.user_settings = data.body.user_settings;
                });

            }
        }
    }
</script>
