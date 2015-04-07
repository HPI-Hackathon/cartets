/* eslint-env browser, jquery */
/* eslint quotes: [2, "single"], strict: 0 */
/* global Handlebars:false */

var cardTemplate;

function card (title, image, location, price, performance, ez, km, consumption) {
    return {
        title: title,
        image: image,
        location: location,
        price: price,
        performance: performance,
        ez: ez,
        km: km,
        consumption: consumption
    };
}

var cards = [
    card('Audi A6', 'http://lorempixel.com/400/300/transport/', 'August-Bebel-Str. 4, 14482 Potsdam', '34000', '140', '2006', '23000', '7'),
    card('VW Polo', 'http://i.ebayimg.com/00/s/NjAwWDgwMA==/z/IVgAAOSwPhdU-FPW/$_8.jpg', 'August-Bebel-Str. 12, 15345 Rehfelde', '5600', '90', '1997', '230000', '6'),
    card('Kaputte Karre', 'http://i.ebayimg.com/00/s/NDgwWDY0MA==/$T2eC16VHJGYFFlLe3qSvBReifcZW2!~~48_8.jpg', 'Großer Stern, 10355 Berlin', '300', '80', '2000', '104000', '14')
];

function templates () {
    cardTemplate = Handlebars.compile($('#card-template').html());
}

function UI () {
    var self = this;
    self.socket = socket;
    self.player = {
        name: ''
    };
    self.position = null;

    self.$allViews = $('.startView, .compareView, .cardView, .waitingView');

    $('#usernameForm').submit(function (e) {
        e.preventDefault();
        var data = {
            action: 'init',
            name: '',
            data: {
                lat: self.position.lat,
                long: self.position.lng
            }
        };

        if ($.trim($('#usernameForm #username').val()) === '') {
            alert('kein Username eingegeben');
        } else {
            data.name = $.trim($('#usernameForm #username').val());
            self.player.name = data.name;
            self.socket.send(JSON.stringify(data));
        }
    });

    $('.cardView').on('click', 'button', function () {
        self.disableCardButtons();
        var attributeToCompare = $(this).data('attribute');
        self.socket.send(JSON.stringify({
            action: 'attributeSelected',
            name: self.player.name,
            data: {
                attributeToCompare: attributeToCompare
            }
        }));
    });

    navigator.geolocation.getCurrentPosition(
        function (position) {
            self.setPosition(position);
        },
        self.positionError
    );

    // UI stuff
    templates();
    //self.createCompareView(cards);
    //self.createCardView(cards[0]);

    self.socket = new WebSocket('ws://localhost:8080', []);

    self.socket.onopen = function () {
        console.info('connected to server');
    };

    // Log errors
    self.socket.onerror = function (error) {
        console.log('WebSocket Error ' + error);
    };

    // Log messages from the server
    self.socket.onmessage = function (e) {
        // e is event object
        // server message is in e.data
        var response = JSON.parse(e.data);
        switch (response.action) {
            case 'accepted':
                UI.activateView('.waitingView');
                break;
            case 'start':
            case 'next':
                UI.createCardView(response.data.card);
                UI.setActivePlayer(response.data.turn);
                break;
            default:
                break;
        }
    };
}

UI.prototype.setPosition = function (position) {
    this.position = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
    $('#locationMessage').hide();
    $('#usernameForm').show();
};

UI.prototype.positionError = function (err) {
    var message = '';
    if (err.code === 1) {
        message = 'Du musst deinen Standort mitteilen, um spielen zu k\u00f6nnen.';
    } else if (err.code === 2) {
        message = 'Dein Standort konnte nicht ermittelt werden.';
    }
    $('#locationMessage')
        .removeClass('panel-default')
        .addClass('panel-danger');
    $('#locationMessage .panel-body').html(message);
    console.log(err.code);
};

UI.prototype.createCompareView = function (cards) {
    this.activateView('.compareView');

    cards.forEach(function (e) {
        $('.compareView').append(cardTemplate(e));
    });
};

UI.prototype.createCardView = function (card) {
    this.activateView('.cardView');

    $('.cardView').append(cardTemplate(card));
};

UI.prototype.activateView = function (view) {
    this.$allViews.hide();
    $(view).show();
};

UI.prototype.setActivePlayer = function (playerName) {
    if (playerName !== self.player.name) {
        UI.disableCardButtons();
    }
};

UI.prototype.disableCardButtons = function () {
    $('.card button').addClass('disabled');
};

var userInterface = new UI();
