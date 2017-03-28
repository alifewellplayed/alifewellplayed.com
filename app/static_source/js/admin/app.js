/*jshint esversion: 6 */

import Vue from 'vue';
import VueRouter from 'vue-router';
import VueResource from 'vue-resource';

Vue.use(VueRouter);
Vue.use(VueResource);
Vue.use(require('vue-moment'));

// CSRF Stuff
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

Vue.http.interceptors.push(function (request, next) {
    request.headers.set('X-CSRFToken', getCookie('csrftoken'));
    next();
});

// require a *.vue component
import App from '../../vue/app.vue';
import SiteSettings from '../../vue/settings.vue';
import Home from '../../vue/dashboard.vue';
import Pages from '../../vue/pages.vue';
import MediaGallery from '../../vue/media.vue';
import Entries from '../../vue/entries.vue';
import NotFound from '../../vue/notfound.vue';
import Editor from '../../vue/editor.vue';
import Topics from '../../vue/topics.vue';
import TopicDetail from '../../vue/topic-detail.vue';
import Channels from '../../vue/channels.vue';
import ChannelDetail from '../../vue/channel-detail.vue';

//Contrib
import NotesDashboard from '../../vue/contrib/micro/home.vue'
import Notes from '../../vue/contrib/micro/note.vue'

// router
const routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/settings', component: SiteSettings, name: 'SiteSettings' },
    { path: '/editor', component: Editor, name: 'EntryNew' },
    { path: '/editor/:entryID', component: Editor, name: 'EntryEdit', },
    { path: '/pages', component: Pages, name: 'PagesList' },
    { path: '/media', component: MediaGallery, name: 'MediaList' },
    { path: '/entries', component: Entries, name: 'EntryList', },
    { path: '/entries/:entryID', component: Entries, name: 'EntryDetail',},
    { path: '/topics', component: Topics, name: 'TopicList' },
    { path: '/topics/:id', component: TopicDetail, name: 'TopicDetail' },
    { path: '/create/topic', component: TopicDetail },
    { path: '/channels', component: Channels, name: 'ChannelList' },
    { path: '/channels:id', component: ChannelDetail, name: 'ChannelDetail' },
    { path: '/create/channel', component: ChannelDetail },
    { path: '/404', component: NotFound, name: 'Error404' },

    //Contrib
    { path: '/notes', component: NotesDashboard, name: 'NotesHome'},
    { path: '/notes/status/:NoteID', component: Notes, name: 'NotesDetail'},

];
const router = new VueRouter({
    routes, // short for routes: routes
    mode: 'history',
    linkActiveClass: 'active',
    base: '/replica/',
});

const app = new Vue({
    router,
    render: (h) => h(App)
}).$mount('#app');
