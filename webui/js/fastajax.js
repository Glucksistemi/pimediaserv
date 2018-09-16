function paramsToString(obj) {
    var str = [];
    for (var item in obj) {
        str.push(item+'='+obj[item])
    }
    return str.join('&')
}

function isEmptyObject(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

var ajax = {
    query: function (method, url, params, onload, onerror, onprogress, sent_json) {
        method = method.toUpperCase();
        if (params !== undefined) {
            paramstr = paramsToString(params)
        } else {
            paramstr = ''
        }
        var request = new XMLHttpRequest();
        request.method = method;
        if (request.method === 'GET') {
            if (paramstr) {
                url = url + '?' + paramstr
            }
        }
        request.open(method, url, true);
        request.onsuccess = onload;
        request.onload = function () {
            if (this.status < 400) {
                this.onsuccess()
            } else {
                this.onerror()
            }
        };
        request.onerror = onerror;
        request.onprogress = onprogress;
        if (method === 'POST') {
            if (sent_json) {
                request.send(JSON.stringify(params))
            } else {
                request.send(paramstr)
            }
        }
        else {
            request.send()
        }
        return request
    },
    get: function (url, params, onload, onerror, onprogress) { //shortcut
        //yes, a bit messy idea about skipping the params part, but... why not?
        if (typeof params === 'function') {
            return this.query('GET', url, {}, params, onload, onerror)
        } else if (typeof params === 'object') {
            return this.query('GET', url, params, onload, onerror, onprogress)
        }
    },
    post: function (url, params, onload, onerror, onprogress) { //shortcut
        return this.query('POST', url, params, onload, onerror, onprogress)
    },
    sendJson: function (url, params, onload, onerror, onprogress) {
        return this.query('POST', url, params, onload, onerror, onprogress, true)
    }
};