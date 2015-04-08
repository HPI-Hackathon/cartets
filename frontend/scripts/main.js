/* eslint-env browser, jquery */
/* eslint quotes: [2, "single"], strict: 0 */
/* global Handlebars:false */

var cardTemplate;

function templates () {
    cardTemplate = Handlebars.compile($('#card-template').html());
    Handlebars.registerHelper('trimString', function(passedString) {
        var theString = passedString.substring(0, 20);
        if (theString !== passedString) {
            theString += '&hellip;';
        }
        return new Handlebars.SafeString(theString);
    });
}

function UI () {
    var self = this;
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
            alert('Bitte gib einen Usernamen ein.');
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

    templates();

    // server: 87.106.33.22
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
        console.log('Server: ', e.data);

        var response = JSON.parse(e.data);
        switch (response.action) {
            case 'accepted':
                self.activateView('.waitingView');
                break;
            case 'playerLost':
                if (response.data.loser.indexOf(self.player.name) > -1) {
                    self.activateView('.loseView');
                    self.socket.onmessage = undefined;
                    break;
                } else if (response.data.loser.indexOf(self.player.name) === -1 && response.data.loser.length >= 2) {
                    self.activateView('.winView');
                    self.socket.onmessage = undefined;
                    break;
                }
            case 'start':
            case 'next':
                if (response.data.winner_card) {
                    self.createCompareView(
                        response.data.all_cards,
                        response.data.winner_card,
                        response.data.attribute_compared,
                        response.data.card,
                        response.data.turn);
                } else {
                    self.startNextRound(response.data.card, response.data.turn);
                }
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

UI.prototype.createCompareView = function (cards, winnerCard, attributeCompared, nextCard, nextTurn) {
    var self = this;
    self.activateView('.compareView');
    $('.compareView').html('');

    cards.forEach(function (e) {
        $('.compareView').append(cardTemplate(e));
    });

    self.disableCardButtons();

    $('.card button[data-attribute="' + attributeCompared + '"]').addClass('btn-primary');

    $($('.card a[href="' + winnerCard.url + '"]').parents('.card')[0]).addClass('winner');

    if (nextCard !== undefined) {
        var endTime = Date.now() + 9000;
        $('.progress').show();
        var interval = setInterval(function () {
            var currentTime = Date.now();
            if (currentTime > endTime) {
                clearInterval(interval);
                $('.progress .progress-bar').width('100%');
                $('.progress').hide();
                self.startNextRound(nextCard, nextTurn);
            } else {
                $('.progress .progress-bar').width(((endTime - currentTime) / 90).toString() + '%');
            }
        }, 75);
    }
};

UI.prototype.createCardView = function (card) {
    this.activateView('.cardView');

    $('.cardView').html(cardTemplate(card));
};

UI.prototype.activateView = function (view) {
    this.$allViews.hide();
    $('#instruction').hide();
    $(view).show();
};

UI.prototype.setInstruction = function (text, type) {
    $('#instruction')
        .show()
        .removeClass()
        .addClass('alert')
        .addClass(type)
        .html(text);
};

UI.prototype.setActivePlayer = function (playerName) {
    if (playerName !== this.player.name) {
        this.disableCardButtons();
        this.setInstruction('Warte auf die Wahl der Kennzahl!', 'alert-info');
    } else {
        this.setInstruction('Nice! Wähle eine Kennzahl!', 'alert-success');
    }
};

UI.prototype.disableCardButtons = function () {
    $('.card button').addClass('disabled');
};

UI.prototype.startNextRound = function (card, turn) {
    this.createCardView(card);
    this.setActivePlayer(turn);
};

var userInterface = new UI();
