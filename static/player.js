var Player = function(tracks)
{
    var self = this;
    self.tracks = tracks;
    self.index = 0

    for (var id = 0; id < self.tracks.length; id++)
    {
        window['title' + id].innerHTML = self.tracks[id].name;
        window['track' + id].addEventListener('click', function(index)
        {
            var isNotPlaying = (self.tracks[index].howl && !self.tracks[index].howl.playing());

            player.stop(index);

            if (isNotPlaying || !self.tracks[index].howl)
            {
                player.play(index);

                window['playbtn'].innerHTML = "||";
            }
        }.bind(self, id));
    }

    window['playbtn'].addEventListener('click', function()
    {
        var isNotPlaying = (self.tracks[self.index].howl && !self.tracks[self.index].howl.playing());

        player.stop(self.index);

        if (isNotPlaying || !self.tracks[self.index].howl)
        {
            window['playbtn'].innerHTML = ">";

            player.play(self.index);
        }
        else
        {
            window['playbtn'].innerHTML = "||";
        }
    });

    window['prevbtn'].addEventListener('click', function()
    {
        player.prev(self.index);
    });

    window['nextbtn'].addEventListener('click', function()
    {
        player.next(self.index);
    });

    window['volume'].addEventListener('input', function()
    {
        var volume = window['volume'].value;

        Howler.volume(volume / 100);

        window['volume'].innerHTML = volume;
    });
};

Player.prototype = {
    
    next: function()
    {
        var self = this;
        var sound = self.tracks[self.index].howl;
        
        self.toggleDisplay(self.index, false);

        index = self.index + 1;
        index = index > (self.tracks.length - 1) ? 0 : index;
        
        if (sound)
        {
            
            sound.stop();
            self.play(index);
        }
    },

    prev: function()
    {
        var self = this;
        var sound = self.tracks[self.index].howl;
        
        self.toggleDisplay(self.index, false);

        index = self.index - 1;
        index = index < 0 ? (self.tracks.length - 1) : index;
        
        if (sound)
        {
            
            sound.stop();
            self.play(index);
        }
    },

    play: function(index)
    {
        var self = this;
        var sound;

        index = typeof index === 'number' ? index : self.index;
        var data = self.tracks[index];

        if (data.howl)
        {
            sound = data.howl;
        }
        else
        {
            sound = data.howl = new Howl({
                src: data.url,
                html: true,
                format: ['mp3', 'flac'],
                onend: function()
                {
                    self.next();
                }
            });
        }

        sound.play();
        self.toggleDisplay(index, true);
        self.index = index;
    },

    stop: function(index)
    {
        var self = this;
        var sound = self.tracks[self.index].howl;
        
        self.toggleDisplay(self.index, false);

        if (sound)
        {
            if (index === self.index)
            {
                sound.pause()
            }
            else
            {
                sound.stop()
            }
        }
    },

    toggleDisplay: function(index, state)
    {
        var self = this;

        window['track' + index].style.backgroundColor = state ? 'rgba(255, 255, 255, 0.33)' : '';
    }
};

