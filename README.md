yosemite_dnsfix
===============

With the release of OS X 10.10 Yosemite, it appears those no good bush whackin’ barracudas at Apple
have put the final nail in the coffin of their crippled DNS search domain functionality.

Specifically, search domains don't work at all for any name containing `"."`, and I'm not aware of
any simple workaround.

In Lion/Mavericks, we could at least fix this by adding `-AlwaysAppendSearchDomains` to the
`mDNSResponder` launchd args, but with the switch to `discoveryd` it seems the muley-headed
mavericks have removed even that small consolation.

Dem's fight'n words!  I suggest you complain to those lily-livered, bow-legged varmints through [any](https://www.apple.com/feedback/macosx.html) [available](https://developer.apple.com/bug-reporting/) [channel](https://bugreport.apple.com/) so
that we don't have to resort to hacks like this.

`yosemite_dnsfix` abuses the `twisted.names` DNS server and `/etc/resolver/` functionality (both present in OS X)
to restore (some of) this basic DNS functionality, which works in all other OSes by default.


Now quit stallin’ and start roastin’!
-------------------------------------

`yosemite_dnsfix` runs a patched `twisted.names` DNS server on localhost that automatically appends a search domain
to all queries before forwarding them to the system nameservers (read periodically from `/etc/resolv.conf`).
When combined with `resolver(5)` config files, this can kind of be used to simulate a sane client resolver.

For example, let's say your company has hostnames that follow a scheme like this:

- server1.env1.example.com
- server1.env2.example.com
- server1.env3.example.com
- ...

You obviously want to be able to resolve these as `server1.env1`, `server1.env2` etc - or do you like RSI?

So, run `yosemite_dnsfix`:

```bash
sudo -i
cd /opt
git clone https://github.com/joedj/yosemite_dnsfix.git
cd yosemite_dnsfix
twistd --nodaemon --uid=_mdnsresponder --gid=_mdnsresponder yosemite_dnsfix --interface=127.0.0.1 --recursive --search-domain=.example.com
```

And then set up your `/etc/resolver/` files:

```bash
sudo -i
for env in env1 env2 env3; do
    echo 'nameserver 127.0.0.1' > /etc/resolver/$env
done
```

Blast your ornery hide, if ya does that just once more... I ain’t a-going after it
----------------------------------------------------------------------------------

You'll want to start it on boot, so edit the included `net.joedj.yosemite_dnsfix.plist`, and then:

```bash
sudo -i
cp /opt/yosemite_dnsfix/net.joedj.yosemite_dnsfix.plist /Library/LaunchDaemons/
launchctl load -w /Library/LaunchDaemons/net.joedj.yosemite_dnsfix.plist
```
