/* eslint-env browser, jquery */
/* eslint quotes: [2, "single"], strict: 0 */

var connection = new WebSocket('ws://localhost:8080', []);

connection.onopen = function () {
    connection.send('Ping');
    console.info('connected to server');
};

// Log errors
connection.onerror = function (error) {
    console.log('WebSocket Error ' + error);
};

// // Log messages from the server
// connection.onmessage = function (e) {
//     // e is event object
//     // server message is in e.data
//     console.log('Server: ' + e.data);
// };

function UI (socket) {
    var self = this;
    self.socket = socket;
    self.player = {
        name: ''
    };
    self.position = null;

    self.setPosition = function (position) {
        console.log('got position');
        self.position = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        $('#locationMessage').hide();
        $('#usernameForm').show();
    };

    self.positionError = function (err) {
        var message = '';
        if (err.code === 1) {
            message = 'Du musst deinen Standort mitteilen, um spielen zu können.';
        } else if (err.code === 2) {
            message = 'Dein Standort konnte nicht ermittelt werden.';
        }
        $('#locationMessage')
            .removeClass('panel-default')
            .addClass('panel-danger');
        $('#locationMessage .panel-body').html(message);
        console.log(err.code);
    };

    $('#usernameForm').submit(function (e) {
        var data = {
            action: 'start',
            username: '',
            lat: self.position.latitude,
            lng: self.position.longitude
        };
        e.preventDefault();
        if ($.trim($('#usernameForm #username').val()) === '') {
            alert('kein Username eingegeben');
        } else {
            self.socket.send(JSON.stringify(data));
        }
    });

    navigator.geolocation.getCurrentPosition(self.setPosition, self.positionError);
}

var userInterface = new UI(connection);
