/**
 * Created by gluck on 04.08.18.
 */
var sysurl = 'http://localhost:5000';
var vuedata = {
    el: '#container',
    data: {
        player_state: false,
        playing_file: null,
        position: 0,
        paused: false,
        volume: 0,
        view: 'index',
        nav_path: '',
        nav_root: -1,
        nav_roots: [],
        nav_folders: [],
        nav_files: [],
        nav_loading: true
    },
    mounted: function () {
        this.$nextTick(function() {
            this.updateStatus();
            vm = this;
            ticks = 0;
            setInterval(function () {
                if (vm.playing_file && !vm.paused) {
                    vm.position++;
                    ticks++;
                    if (!(ticks % 20)) {
                        vm.updateStatus()
                    }
                }
            }, 1000)
        })
    },
    methods: {
        setOffset: function (event) {
            vm = this;
            ajax.get(sysurl+'/control', {command: 'seek', value: event.target.value});
            event.target.value = 0;
        },
        getRoots: function() {
            var vm = this;
            this.nav_loading = true;
            ajax.get(sysurl+'/navigate', function () {
                vm.nav_loading = false;
                vm.nav_roots = JSON.parse(this.responseText)
            })
        },
        getFolderContains: function (folder) {
            var vm = this;
            this.nav_loading = true;
            var parseResponse = function () {
                var res = JSON.parse(this.responseText);
                    vm.nav_loading = false;
                    vm.nav_folders = res.folders;
                    vm.nav_files = res.files;
                    //eeeeeeah inline if inside inline if, what could be better?
                    vm.nav_path = (vm.nav_path ? (folder ? [vm.nav_path, folder].join('/') : vm.nav_path) : folder)
            };
            if (!folder) {
                ajax.get(sysurl+'/navigate', {root: this.nav_root, path: this.nav_path}, parseResponse)
            }
            else {
                ajax.get(sysurl+'/navigate', {
                    root: this.nav_root,
                    path: (this.nav_path ? [this.nav_path, folder].join('/') : folder)
                }, parseResponse)
            }
        },
        navUp: function () {
            if (!this.nav_path) {
                this.nav_root = -1;
                this.getRoots();
                return
            }
            var tmp_pth = this.nav_path.split('/').slice(0, -1).join('/');
            console.log(tmp_pth, this.nav_path);
            if (tmp_pth == this.nav_path) {
                this.nav_path = ''
            } else {
                this.nav_path = tmp_pth
            }
            this.getFolderContains()
        },
        setRoot: function (idx) {
            this.nav_root = idx;
            this.getFolderContains('')

        },
        switchView: function (view) {
            this.view = view;
            if (view === 'navigation' && this.nav_root === -1) {
                this.getRoots()
            }
        },
        playFile: function (filename) {
            vm = this;
            ajax.get(sysurl+'/play', {
                root: this.nav_root,
                content: (this.nav_path ? [this.nav_path, filename].join('/') : filename)
            }, function () {
                res = JSON.parse(this.responseText);
                if (res.error) {
                    alert(res.error_data)
                } else {
                    vm.player_state = true;
                    vm.playing_file = res.filename;
                    vm.switchView('index')
                }
            })
        },
        updateStatus: function () {
            vm = this;
            ajax.get(sysurl + '/status', {}, function () {
                var status = JSON.parse(this.responseText);
                if (!status.error) {
                    vm.player_state = status.mplayer_on;
                    if (status.mplayer_on) {
                        vm.position = Number(status.position.seconds);
                        vm.playing_file = status.filename;
                        vm.volume = Number(status.volume);
                        vm.paused = status.paused === 'yes';
                    } else {
                        vm.position = 0;
                        vm.playing_file = null;
                        vm.volume = 0;
                        vm.paused = false
                    }
                }
            })
        },
        switchPause: function () {
            vm = this;
            ajax.get(sysurl + '/control', {'command': 'pause'}, function () {
                vm.updateStatus()
            })
        },
        setVolume: function (event) {
            vm = this;
            ajax.get(sysurl + '/props', {'property': 'volume', 'mode': 'set', 'value': this.volume}, function () {
                vm.updateStatus()
            })
        },
        nextSubtitles: function () {
            vm = this;
            ajax.get(sysurl + '/control', {'command': 'sub_select'}, function () {
                vm.updateStatus()
            })
        },
        nextAudio: function () {
            vm = this;
            ajax.get(sysurl + '/control', {'command': 'switch_audio'}, function () {
                vm.updateStatus()
            })
        }
    }
};