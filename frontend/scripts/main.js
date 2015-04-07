/* eslint-env browser, jquery */
/* eslint quotes: [2, "single"], strict: 0 */

var connection = new WebSocket('ws://localhost:8080', []);

// connection.onopen = function () {
//     connection.send('Ping');
//     console.info('connected to server');
// };

// // Log errors
// connection.onerror = function (error) {
//     console.log('WebSocket Error ' + error);
// };

// // Log messages from the server
// connection.onmessage = function (e) {
//     // e is event object
//     // server message is in e.data
//     console.log('Server: ' + e.data);
// };

function UI () {
    var self = this;
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
    };

    self.positionError = function (err) {
        console.log(err.code);
    };

    navigator.geolocation.getCurrentPosition(self.setPosition, self.positionError);
}

var userInterface = new UI();
