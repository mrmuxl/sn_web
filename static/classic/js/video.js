(function(window, undefined) {
    function isArraylike(a) {
        var b = a.length,
        c = jQuery.type(a);
        return jQuery.isWindow(a) ? !1 : a.nodeType === 1 && b ? !0 : c === "array" || c !== "function" && (b === 0 || typeof b == "number" && b > 0 && b - 1 in a)
    }
    function createOptions(a) {
        var b = optionsCache[a] = {};
        return jQuery.each(a.match(core_rnotwhite) || [],
        function(a, c) {
            b[c] = !0
        }),
        b
    }
    function Data() {
        Object.defineProperty(this.cache = {},
        0, {
            get: function() {
                return {}
            }
        }),
        this.expando = jQuery.expando + Math.random()
    }
    function dataAttr(a, b, c) {
        var d;
        if (c === undefined && a.nodeType === 1) {
            d = "data-" + b.replace(rmultiDash, "-$1").toLowerCase(),
            c = a.getAttribute(d);
            if (typeof c == "string") {
                try {
                    c = c === "true" ? !0 : c === "false" ? !1 : c === "null" ? null: +c + "" === c ? +c: rbrace.test(c) ? JSON.parse(c) : c
                } catch(e) {}
                data_user.set(a, b, c)
            } else c = undefined
        }
        return c
    }
    function returnTrue() {
        return ! 0
    }
    function returnFalse() {
        return ! 1
    }
    function safeActiveElement() {
        try {
            return document.activeElement
        } catch(a) {}
    }
    function sibling(a, b) {
        while ((a = a[b]) && a.nodeType !== 1);
        return a
    }
    function winnow(a, b, c) {
        if (jQuery.isFunction(b)) return jQuery.grep(a,
        function(a, d) {
            return !! b.call(a, d, a) !== c
        });
        if (b.nodeType) return jQuery.grep(a,
        function(a) {
            return a === b !== c
        });
        if (typeof b == "string") {
            if (isSimple.test(b)) return jQuery.filter(b, a, c);
            b = jQuery.filter(b, a)
        }
        return jQuery.grep(a,
        function(a) {
            return core_indexOf.call(b, a) >= 0 !== c
        })
    }
    function manipulationTarget(a, b) {
        return jQuery.nodeName(a, "table") && jQuery.nodeName(b.nodeType === 1 ? b: b.firstChild, "tr") ? a.getElementsByTagName("tbody")[0] || a.appendChild(a.ownerDocument.createElement("tbody")) : a
    }
    function disableScript(a) {
        return a.type = (a.getAttribute("type") !== null) + "/" + a.type,
        a
    }
    function restoreScript(a) {
        var b = rscriptTypeMasked.exec(a.type);
        return b ? a.type = b[1] : a.removeAttribute("type"),
        a
    }
    function setGlobalEval(a, b) {
        var c = a.length,
        d = 0;
        for (; d < c; d++) data_priv.set(a[d], "globalEval", !b || data_priv.get(b[d], "globalEval"))
    }
    function cloneCopyEvent(a, b) {
        var c, d, e, f, g, h, i, j;
        if (b.nodeType !== 1) return;
        if (data_priv.hasData(a)) {
            f = data_priv.access(a),
            g = jQuery.extend({},
            f),
            j = f.events,
            data_priv.set(b, g);
            if (j) {
                delete g.handle,
                g.events = {};
                for (e in j) for (c = 0, d = j[e].length; c < d; c++) jQuery.event.add(b, e, j[e][c])
            }
        }
        data_user.hasData(a) && (h = data_user.access(a), i = jQuery.extend({},
        h), data_user.set(b, i))
    }
    function getAll(a, b) {
        var c = a.getElementsByTagName ? a.getElementsByTagName(b || "*") : a.querySelectorAll ? a.querySelectorAll(b || "*") : [];
        return b === undefined || b && jQuery.nodeName(a, b) ? jQuery.merge([a], c) : c
    }
    function fixInput(a, b) {
        var c = b.nodeName.toLowerCase();
        if (c === "input" && manipulation_rcheckableType.test(a.type)) b.checked = a.checked;
        else if (c === "input" || c === "textarea") b.defaultValue = a.defaultValue
    }
    function vendorPropName(a, b) {
        if (b in a) return b;
        var c = b.charAt(0).toUpperCase() + b.slice(1),
        d = b,
        e = cssPrefixes.length;
        while (e--) {
            b = cssPrefixes[e] + c;
            if (b in a) return b
        }
        return d
    }
    function isHidden(a, b) {
        return a = b || a,
        jQuery.css(a, "display") === "none" || !jQuery.contains(a.ownerDocument, a)
    }
    function getStyles(a) {
        return window.getComputedStyle(a, null)
    }
    function showHide(a, b) {
        var c, d, e, f = [],
        g = 0,
        h = a.length;
        for (; g < h; g++) {
            d = a[g];
            if (!d.style) continue;
            f[g] = data_priv.get(d, "olddisplay"),
            c = d.style.display,
            b ? (!f[g] && c === "none" && (d.style.display = ""), d.style.display === "" && isHidden(d) && (f[g] = data_priv.access(d, "olddisplay", css_defaultDisplay(d.nodeName)))) : f[g] || (e = isHidden(d), (c && c !== "none" || !e) && data_priv.set(d, "olddisplay", e ? c: jQuery.css(d, "display")))
        }
        for (g = 0; g < h; g++) {
            d = a[g];
            if (!d.style) continue;
            if (!b || d.style.display === "none" || d.style.display === "") d.style.display = b ? f[g] || "": "none"
        }
        return a
    }
    function setPositiveNumber(a, b, c) {
        var d = rnumsplit.exec(b);
        return d ? Math.max(0, d[1] - (c || 0)) + (d[2] || "px") : b
    }
    function augmentWidthOrHeight(a, b, c, d, e) {
        var f = c === (d ? "border": "content") ? 4 : b === "width" ? 1 : 0,
        g = 0;
        for (; f < 4; f += 2) c === "margin" && (g += jQuery.css(a, c + cssExpand[f], !0, e)),
        d ? (c === "content" && (g -= jQuery.css(a, "padding" + cssExpand[f], !0, e)), c !== "margin" && (g -= jQuery.css(a, "border" + cssExpand[f] + "Width", !0, e))) : (g += jQuery.css(a, "padding" + cssExpand[f], !0, e), c !== "padding" && (g += jQuery.css(a, "border" + cssExpand[f] + "Width", !0, e)));
        return g
    }
    function getWidthOrHeight(a, b, c) {
        var d = !0,
        e = b === "width" ? a.offsetWidth: a.offsetHeight,
        f = getStyles(a),
        g = jQuery.support.boxSizing && jQuery.css(a, "boxSizing", !1, f) === "border-box";
        if (e <= 0 || e == null) {
            e = curCSS(a, b, f);
            if (e < 0 || e == null) e = a.style[b];
            if (rnumnonpx.test(e)) return e;
            d = g && (jQuery.support.boxSizingReliable || e === a.style[b]),
            e = parseFloat(e) || 0
        }
        return e + augmentWidthOrHeight(a, b, c || (g ? "border": "content"), d, f) + "px"
    }
    function css_defaultDisplay(a) {
        var b = document,
        c = elemdisplay[a];
        if (!c) {
            c = actualDisplay(a, b);
            if (c === "none" || !c) iframe = (iframe || jQuery("<iframe frameborder='0' width='0' height='0'/>").css("cssText", "display:block !important")).appendTo(b.documentElement),
            b = (iframe[0].contentWindow || iframe[0].contentDocument).document,
            b.write("<!doctype html><html><body>"),
            b.close(),
            c = actualDisplay(a, b),
            iframe.detach();
            elemdisplay[a] = c
        }
        return c
    }
    function actualDisplay(a, b) {
        var c = jQuery(b.createElement(a)).appendTo(b.body),
        d = jQuery.css(c[0], "display");
        return c.remove(),
        d
    }
    function buildParams(a, b, c, d) {
        var e;
        if (jQuery.isArray(b)) jQuery.each(b,
        function(b, e) {
            c || rbracket.test(a) ? d(a, e) : buildParams(a + "[" + (typeof e == "object" ? b: "") + "]", e, c, d)
        });
        else if (!c && jQuery.type(b) === "object") for (e in b) buildParams(a + "[" + e + "]", b[e], c, d);
        else d(a, b)
    }
    function addToPrefiltersOrTransports(a) {
        return function(b, c) {
            typeof b != "string" && (c = b, b = "*");
            var d, e = 0,
            f = b.toLowerCase().match(core_rnotwhite) || [];
            if (jQuery.isFunction(c)) while (d = f[e++]) d[0] === "+" ? (d = d.slice(1) || "*", (a[d] = a[d] || []).unshift(c)) : (a[d] = a[d] || []).push(c)
        }
    }
    function inspectPrefiltersOrTransports(a, b, c, d) {
        function g(h) {
            var i;
            return e[h] = !0,
            jQuery.each(a[h] || [],
            function(a, h) {
                var j = h(b, c, d);
                if (typeof j == "string" && !f && !e[j]) return b.dataTypes.unshift(j),
                g(j),
                !1;
                if (f) return ! (i = j)
            }),
            i
        }
        var e = {},
        f = a === transports;
        return g(b.dataTypes[0]) || !e["*"] && g("*")
    }
    function ajaxExtend(a, b) {
        var c, d, e = jQuery.ajaxSettings.flatOptions || {};
        for (c in b) b[c] !== undefined && ((e[c] ? a: d || (d = {}))[c] = b[c]);
        return d && jQuery.extend(!0, a, d),
        a
    }
    function ajaxHandleResponses(a, b, c) {
        var d, e, f, g, h = a.contents,
        i = a.dataTypes;
        while (i[0] === "*") i.shift(),
        d === undefined && (d = a.mimeType || b.getResponseHeader("Content-Type"));
        if (d) for (e in h) if (h[e] && h[e].test(d)) {
            i.unshift(e);
            break
        }
        if (i[0] in c) f = i[0];
        else {
            for (e in c) {
                if (!i[0] || a.converters[e + " " + i[0]]) {
                    f = e;
                    break
                }
                g || (g = e)
            }
            f = f || g
        }
        if (f) return f !== i[0] && i.unshift(f),
        c[f]
    }
    function ajaxConvert(a, b, c, d) {
        var e, f, g, h, i, j = {},
        k = a.dataTypes.slice();
        if (k[1]) for (g in a.converters) j[g.toLowerCase()] = a.converters[g];
        f = k.shift();
        while (f) {
            a.responseFields[f] && (c[a.responseFields[f]] = b),
            !i && d && a.dataFilter && (b = a.dataFilter(b, a.dataType)),
            i = f,
            f = k.shift();
            if (f) if (f === "*") f = i;
            else if (i !== "*" && i !== f) {
                g = j[i + " " + f] || j["* " + f];
                if (!g) for (e in j) {
                    h = e.split(" ");
                    if (h[1] === f) {
                        g = j[i + " " + h[0]] || j["* " + h[0]];
                        if (g) {
                            g === !0 ? g = j[e] : j[e] !== !0 && (f = h[0], k.unshift(h[1]));
                            break
                        }
                    }
                }
                if (g !== !0) if (g && a["throws"]) b = g(b);
                else try {
                    b = g(b)
                } catch(l) {
                    return {
                        state: "parsererror",
                        error: g ? l: "No conversion from " + i + " to " + f
                    }
                }
            }
        }
        return {
            state: "success",
            data: b
        }
    }
    function createFxNow() {
        return setTimeout(function() {
            fxNow = undefined
        }),
        fxNow = jQuery.now()
    }
    function createTweens(a, b) {
        jQuery.each(b,
        function(b, c) {
            var d = (tweeners[b] || []).concat(tweeners["*"]),
            e = 0,
            f = d.length;
            for (; e < f; e++) if (d[e].call(a, b, c)) return
        })
    }
    function Animation(a, b, c) {
        var d, e, f = 0,
        g = animationPrefilters.length,
        h = jQuery.Deferred().always(function() {
            delete i.elem
        }),
        i = function() {
            if (e) return ! 1;
            var b = fxNow || createFxNow(),
            c = Math.max(0, j.startTime + j.duration - b),
            d = c / j.duration || 0,
            f = 1 - d,
            g = 0,
            i = j.tweens.length;
            for (; g < i; g++) j.tweens[g].run(f);
            return h.notifyWith(a, [j, f, c]),
            f < 1 && i ? c: (h.resolveWith(a, [j]), !1)
        },
        j = h.promise({
            elem: a,
            props: jQuery.extend({},
            b),
            opts: jQuery.extend(!0, {
                specialEasing: {}
            },
            c),
            originalProperties: b,
            originalOptions: c,
            startTime: fxNow || createFxNow(),
            duration: c.duration,
            tweens: [],
            createTween: function(b, c) {
                var d = jQuery.Tween(a, j.opts, b, c, j.opts.specialEasing[b] || j.opts.easing);
                return j.tweens.push(d),
                d
            },
            stop: function(b) {
                var c = 0,
                d = b ? j.tweens.length: 0;
                if (e) return this;
                e = !0;
                for (; c < d; c++) j.tweens[c].run(1);
                return b ? h.resolveWith(a, [j, b]) : h.rejectWith(a, [j, b]),
                this
            }
        }),
        k = j.props;
        propFilter(k, j.opts.specialEasing);
        for (; f < g; f++) {
            d = animationPrefilters[f].call(j, a, k, j.opts);
            if (d) return d
        }
        return createTweens(j, k),
        jQuery.isFunction(j.opts.start) && j.opts.start.call(a, j),
        jQuery.fx.timer(jQuery.extend(i, {
            elem: a,
            anim: j,
            queue: j.opts.queue
        })),
        j.progress(j.opts.progress).done(j.opts.done, j.opts.complete).fail(j.opts.fail).always(j.opts.always)
    }
    function propFilter(a, b) {
        var c, d, e, f, g;
        for (c in a) {
            d = jQuery.camelCase(c),
            e = b[d],
            f = a[c],
            jQuery.isArray(f) && (e = f[1], f = a[c] = f[0]),
            c !== d && (a[d] = f, delete a[c]),
            g = jQuery.cssHooks[d];
            if (g && "expand" in g) {
                f = g.expand(f),
                delete a[d];
                for (c in f) c in a || (a[c] = f[c], b[c] = e)
            } else b[d] = e
        }
    }
    function defaultPrefilter(a, b, c) {
        var d, e, f, g, h, i, j, k, l, m = this,
        n = a.style,
        o = {},
        p = [],
        q = a.nodeType && isHidden(a);
        c.queue || (k = jQuery._queueHooks(a, "fx"), k.unqueued == null && (k.unqueued = 0, l = k.empty.fire, k.empty.fire = function() {
            k.unqueued || l()
        }), k.unqueued++, m.always(function() {
            m.always(function() {
                k.unqueued--,
                jQuery.queue(a, "fx").length || k.empty.fire()
            })
        })),
        a.nodeType === 1 && ("height" in b || "width" in b) && (c.overflow = [n.overflow, n.overflowX, n.overflowY], jQuery.css(a, "display") === "inline" && jQuery.css(a, "float") === "none" && (n.display = "inline-block")),
        c.overflow && (n.overflow = "hidden", m.always(function() {
            n.overflow = c.overflow[0],
            n.overflowX = c.overflow[1],
            n.overflowY = c.overflow[2]
        })),
        h = data_priv.get(a, "fxshow");
        for (d in b) {
            f = b[d];
            if (rfxtypes.exec(f)) {
                delete b[d],
                i = i || f === "toggle";
                if (f === (q ? "hide": "show")) if (f === "show" && h !== undefined && h[d] !== undefined) q = !0;
                else continue;
                p.push(d)
            }
        }
        g = p.length;
        if (g) {
            h = data_priv.get(a, "fxshow") || data_priv.access(a, "fxshow", {}),
            "hidden" in h && (q = h.hidden),
            i && (h.hidden = !q),
            q ? jQuery(a).show() : m.done(function() {
                jQuery(a).hide()
            }),
            m.done(function() {
                var b;
                data_priv.remove(a, "fxshow");
                for (b in o) jQuery.style(a, b, o[b])
            });
            for (d = 0; d < g; d++) e = p[d],
            j = m.createTween(e, q ? h[e] : 0),
            o[e] = h[e] || jQuery.style(a, e),
            e in h || (h[e] = j.start, q && (j.end = j.start, j.start = e === "width" || e === "height" ? 1 : 0))
        }
    }
    function Tween(a, b, c, d, e) {
        return new Tween.prototype.init(a, b, c, d, e)
    }
    function genFx(a, b) {
        var c, d = {
            height: a
        },
        e = 0;
        b = b ? 1 : 0;
        for (; e < 4; e += 2 - b) c = cssExpand[e],
        d["margin" + c] = d["padding" + c] = a;
        return b && (d.opacity = d.width = a),
        d
    }
    function getWindow(a) {
        return jQuery.isWindow(a) ? a: a.nodeType === 9 && a.defaultView
    }
    var rootjQuery, readyList, core_strundefined = typeof undefined,
    location = window.location,
    document = window.document,
    docElem = document.documentElement,
    _jQuery = window.jQuery,
    _$ = window.$,
    class2type = {},
    core_deletedIds = [],
    core_version = "2.0.0",
    core_concat = core_deletedIds.concat,
    core_push = core_deletedIds.push,
    core_slice = core_deletedIds.slice,
    core_indexOf = core_deletedIds.indexOf,
    core_toString = class2type.toString,
    core_hasOwn = class2type.hasOwnProperty,
    core_trim = core_version.trim,
    jQuery = function(a, b) {
        return new jQuery.fn.init(a, b, rootjQuery)
    },
    core_pnum = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,
    core_rnotwhite = /\S+/g,
    rquickExpr = /^(?:(<[\w\W]+>)[^>]*|#([\w-]*))$/,
    rsingleTag = /^<(\w+)\s*\/?>(?:<\/\1>|)$/,
    rmsPrefix = /^-ms-/,
    rdashAlpha = /-([\da-z])/gi,
    fcamelCase = function(a, b) {
        return b.toUpperCase()
    },
    completed = function() {
        document.removeEventListener("DOMContentLoaded", completed, !1),
        window.removeEventListener("load", completed, !1),
        jQuery.ready()
    };
    jQuery.fn = jQuery.prototype = {
        jquery: core_version,
        constructor: jQuery,
        init: function(a, b, c) {
            var d, e;
            if (!a) return this;
            if (typeof a == "string") {
                a.charAt(0) === "<" && a.charAt(a.length - 1) === ">" && a.length >= 3 ? d = [null, a, null] : d = rquickExpr.exec(a);
                if (d && (d[1] || !b)) {
                    if (d[1]) {
                        b = b instanceof jQuery ? b[0] : b,
                        jQuery.merge(this, jQuery.parseHTML(d[1], b && b.nodeType ? b.ownerDocument || b: document, !0));
                        if (rsingleTag.test(d[1]) && jQuery.isPlainObject(b)) for (d in b) jQuery.isFunction(this[d]) ? this[d](b[d]) : this.attr(d, b[d]);
                        return this
                    }
                    return e = document.getElementById(d[2]),
                    e && e.parentNode && (this.length = 1, this[0] = e),
                    this.context = document,
                    this.selector = a,
                    this
                }
                return ! b || b.jquery ? (b || c).find(a) : this.constructor(b).find(a)
            }
            return a.nodeType ? (this.context = this[0] = a, this.length = 1, this) : jQuery.isFunction(a) ? c.ready(a) : (a.selector !== undefined && (this.selector = a.selector, this.context = a.context), jQuery.makeArray(a, this))
        },
        selector: "",
        length: 0,
        toArray: function() {
            return core_slice.call(this)
        },
        get: function(a) {
            return a == null ? this.toArray() : a < 0 ? this[this.length + a] : this[a]
        },
        pushStack: function(a) {
            var b = jQuery.merge(this.constructor(), a);
            return b.prevObject = this,
            b.context = this.context,
            b
        },
        each: function(a, b) {
            return jQuery.each(this, a, b)
        },
        ready: function(a) {
            return jQuery.ready.promise().done(a),
            this
        },
        slice: function() {
            return this.pushStack(core_slice.apply(this, arguments))
        },
        first: function() {
            return this.eq(0)
        },
        last: function() {
            return this.eq( - 1)
        },
        eq: function(a) {
            var b = this.length,
            c = +a + (a < 0 ? b: 0);
            return this.pushStack(c >= 0 && c < b ? [this[c]] : [])
        },
        map: function(a) {
            return this.pushStack(jQuery.map(this,
            function(b, c) {
                return a.call(b, c, b)
            }))
        },
        end: function() {
            return this.prevObject || this.constructor(null)
        },
        push: core_push,
        sort: [].sort,
        splice: [].splice
    },
    jQuery.fn.init.prototype = jQuery.fn,
    jQuery.extend = jQuery.fn.extend = function() {
        var a, b, c, d, e, f, g = arguments[0] || {},
        h = 1,
        i = arguments.length,
        j = !1;
        typeof g == "boolean" && (j = g, g = arguments[1] || {},
        h = 2),
        typeof g != "object" && !jQuery.isFunction(g) && (g = {}),
        i === h && (g = this, --h);
        for (; h < i; h++) if ((a = arguments[h]) != null) for (b in a) {
            c = g[b],
            d = a[b];
            if (g === d) continue;
            j && d && (jQuery.isPlainObject(d) || (e = jQuery.isArray(d))) ? (e ? (e = !1, f = c && jQuery.isArray(c) ? c: []) : f = c && jQuery.isPlainObject(c) ? c: {},
            g[b] = jQuery.extend(j, f, d)) : d !== undefined && (g[b] = d)
        }
        return g
    },
    jQuery.extend({
        expando: "jQuery" + (core_version + Math.random()).replace(/\D/g, ""),
        noConflict: function(a) {
            return window.$ === jQuery && (window.$ = _$),
            a && window.jQuery === jQuery && (window.jQuery = _jQuery),
            jQuery
        },
        isReady: !1,
        readyWait: 1,
        holdReady: function(a) {
            a ? jQuery.readyWait++:jQuery.ready(!0)
        },
        ready: function(a) {
            if (a === !0 ? --jQuery.readyWait: jQuery.isReady) return;
            jQuery.isReady = !0;
            if (a !== !0 && --jQuery.readyWait > 0) return;
            readyList.resolveWith(document, [jQuery]),
            jQuery.fn.trigger && jQuery(document).trigger("ready").off("ready")
        },
        isFunction: function(a) {
            return jQuery.type(a) === "function"
        },
        isArray: Array.isArray,
        isWindow: function(a) {
            return a != null && a === a.window
        },
        isNumeric: function(a) {
            return ! isNaN(parseFloat(a)) && isFinite(a)
        },
        type: function(a) {
            return a == null ? String(a) : typeof a == "object" || typeof a == "function" ? class2type[core_toString.call(a)] || "object": typeof a
        },
        isPlainObject: function(a) {
            if (jQuery.type(a) !== "object" || a.nodeType || jQuery.isWindow(a)) return ! 1;
            try {
                if (a.constructor && !core_hasOwn.call(a.constructor.prototype, "isPrototypeOf")) return ! 1
            } catch(b) {
                return ! 1
            }
            return ! 0
        },
        isEmptyObject: function(a) {
            var b;
            for (b in a) return ! 1;
            return ! 0
        },
        error: function(a) {
            throw new Error(a)
        },
        parseHTML: function(a, b, c) {
            if (!a || typeof a != "string") return null;
            typeof b == "boolean" && (c = b, b = !1),
            b = b || document;
            var d = rsingleTag.exec(a),
            e = !c && [];
            return d ? [b.createElement(d[1])] : (d = jQuery.buildFragment([a], b, e), e && jQuery(e).remove(), jQuery.merge([], d.childNodes))
        },
        parseJSON: JSON.parse,
        parseXML: function(a) {
            var b, c;
            if (!a || typeof a != "string") return null;
            try {
                c = new DOMParser,
                b = c.parseFromString(a, "text/xml")
            } catch(d) {
                b = undefined
            }
            return (!b || b.getElementsByTagName("parsererror").length) && jQuery.error("Invalid XML: " + a),
            b
        },
        noop: function() {},
        globalEval: function(code) {
            var script, indirect = eval;
            code = jQuery.trim(code),
            code && (code.indexOf("use strict") === 1 ? (script = document.createElement("script"), script.text = code, document.head.appendChild(script).parentNode.removeChild(script)) : indirect(code))
        },
        camelCase: function(a) {
            return a.replace(rmsPrefix, "ms-").replace(rdashAlpha, fcamelCase)
        },
        nodeName: function(a, b) {
            return a.nodeName && a.nodeName.toLowerCase() === b.toLowerCase()
        },
        each: function(a, b, c) {
            var d, e = 0,
            f = a.length,
            g = isArraylike(a);
            if (c) if (g) for (; e < f; e++) {
                d = b.apply(a[e], c);
                if (d === !1) break
            } else for (e in a) {
                d = b.apply(a[e], c);
                if (d === !1) break
            } else if (g) for (; e < f; e++) {
                d = b.call(a[e], e, a[e]);
                if (d === !1) break
            } else for (e in a) {
                d = b.call(a[e], e, a[e]);
                if (d === !1) break
            }
            return a
        },
        trim: function(a) {
            return a == null ? "": core_trim.call(a)
        },
        makeArray: function(a, b) {
            var c = b || [];
            return a != null && (isArraylike(Object(a)) ? jQuery.merge(c, typeof a == "string" ? [a] : a) : core_push.call(c, a)),
            c
        },
        inArray: function(a, b, c) {
            return b == null ? -1 : core_indexOf.call(b, a, c)
        },
        merge: function(a, b) {
            var c = b.length,
            d = a.length,
            e = 0;
            if (typeof c == "number") for (; e < c; e++) a[d++] = b[e];
            else while (b[e] !== undefined) a[d++] = b[e++];
            return a.length = d,
            a
        },
        grep: function(a, b, c) {
            var d, e = [],
            f = 0,
            g = a.length;
            c = !!c;
            for (; f < g; f++) d = !!b(a[f], f),
            c !== d && e.push(a[f]);
            return e
        },
        map: function(a, b, c) {
            var d, e = 0,
            f = a.length,
            g = isArraylike(a),
            h = [];
            if (g) for (; e < f; e++) d = b(a[e], e, c),
            d != null && (h[h.length] = d);
            else for (e in a) d = b(a[e], e, c),
            d != null && (h[h.length] = d);
            return core_concat.apply([], h)
        },
        guid: 1,
        proxy: function(a, b) {
            var c, d, e;
            return typeof b == "string" && (c = a[b], b = a, a = c),
            jQuery.isFunction(a) ? (d = core_slice.call(arguments, 2), e = function() {
                return a.apply(b || this, d.concat(core_slice.call(arguments)))
            },
            e.guid = a.guid = a.guid || jQuery.guid++, e) : undefined
        },
        access: function(a, b, c, d, e, f, g) {
            var h = 0,
            i = a.length,
            j = c == null;
            if (jQuery.type(c) === "object") {
                e = !0;
                for (h in c) jQuery.access(a, b, h, c[h], !0, f, g)
            } else if (d !== undefined) {
                e = !0,
                jQuery.isFunction(d) || (g = !0),
                j && (g ? (b.call(a, d), b = null) : (j = b, b = function(a, b, c) {
                    return j.call(jQuery(a), c)
                }));
                if (b) for (; h < i; h++) b(a[h], c, g ? d: d.call(a[h], h, b(a[h], c)))
            }
            return e ? a: j ? b.call(a) : i ? b(a[0], c) : f
        },
        now: Date.now,
        swap: function(a, b, c, d) {
            var e, f, g = {};
            for (f in b) g[f] = a.style[f],
            a.style[f] = b[f];
            e = c.apply(a, d || []);
            for (f in b) a.style[f] = g[f];
            return e
        }
    }),
    jQuery.ready.promise = function(a) {
        return readyList || (readyList = jQuery.Deferred(), document.readyState === "complete" ? setTimeout(jQuery.ready) : (document.addEventListener("DOMContentLoaded", completed, !1), window.addEventListener("load", completed, !1))),
        readyList.promise(a)
    },
    jQuery.each("Boolean Number String Function Array Date RegExp Object Error".split(" "),
    function(a, b) {
        class2type["[object " + b + "]"] = b.toLowerCase()
    }),
    rootjQuery = jQuery(document),
    function(a, b) {
        function be(a) {
            return Y.test(a + "")
        }
        function bf() {
            var a, b = [];
            return a = function(c, d) {
                return b.push(c += " ") > e.cacheLength && delete a[b.shift()],
                a[c] = d
            }
        }
        function bg(a) {
            return a[s] = !0,
            a
        }
        function bh(a) {
            var b = l.createElement("div");
            try {
                return !! a(b)
            } catch(c) {
                return ! 1
            } finally {
                b.parentNode && b.parentNode.removeChild(b),
                b = null
            }
        }
        function bi(a, b, c, d) {
            var e, f, g, h, i, j, m, p, q, v;
            (b ? b.ownerDocument || b: t) !== l && k(b),
            b = b || l,
            c = c || [];
            if (!a || typeof a != "string") return c;
            if ((h = b.nodeType) !== 1 && h !== 9) return [];
            if (n && !d) {
                if (e = Z.exec(a)) if (g = e[1]) {
                    if (h === 9) {
                        f = b.getElementById(g);
                        if (!f || !f.parentNode) return c;
                        if (f.id === g) return c.push(f),
                        c
                    } else if (b.ownerDocument && (f = b.ownerDocument.getElementById(g)) && r(b, f) && f.id === g) return c.push(f),
                    c
                } else {
                    if (e[2]) return H.apply(c, b.getElementsByTagName(a)),
                    c;
                    if ((g = e[3]) && u.getElementsByClassName && b.getElementsByClassName) return H.apply(c, b.getElementsByClassName(g)),
                    c
                }
                if (u.qsa && (!o || !o.test(a))) {
                    p = m = s,
                    q = b,
                    v = h === 9 && a;
                    if (h === 1 && b.nodeName.toLowerCase() !== "object") {
                        j = bp(a),
                        (m = b.getAttribute("id")) ? p = m.replace(ba, "\\$&") : b.setAttribute("id", p),
                        p = "[id='" + p + "'] ",
                        i = j.length;
                        while (i--) j[i] = p + bq(j[i]);
                        q = T.test(a) && b.parentNode || b,
                        v = j.join(",")
                    }
                    if (v) try {
                        return H.apply(c, q.querySelectorAll(v)),
                        c
                    } catch(w) {} finally {
                        m || b.removeAttribute("id")
                    }
                }
            }
            return by(a.replace(Q, "$1"), b, c, d)
        }
        function bj(a, b) {
            var c = b && a,
            d = c && (~b.sourceIndex || D) - (~a.sourceIndex || D);
            if (d) return d;
            if (c) while (c = c.nextSibling) if (c === b) return - 1;
            return a ? 1 : -1
        }
        function bk(a, c, d) {
            var e;
            return d ? b: (e = a.getAttributeNode(c)) && e.specified ? e.value: a[c] === !0 ? c.toLowerCase() : null
        }
        function bl(a, c, d) {
            var e;
            return d ? b: e = a.getAttribute(c, c.toLowerCase() === "type" ? 1 : 2)
        }
        function bm(a) {
            return function(b) {
                var c = b.nodeName.toLowerCase();
                return c === "input" && b.type === a
            }
        }
        function bn(a) {
            return function(b) {
                var c = b.nodeName.toLowerCase();
                return (c === "input" || c === "button") && b.type === a
            }
        }
        function bo(a) {
            return bg(function(b) {
                return b = +b,
                bg(function(c, d) {
                    var e, f = a([], c.length, b),
                    g = f.length;
                    while (g--) c[e = f[g]] && (c[e] = !(d[e] = c[e]))
                })
            })
        }
        function bp(a, b) {
            var c, d, f, g, h, i, j, k = y[a + " "];
            if (k) return b ? 0 : k.slice(0);
            h = a,
            i = [],
            j = e.preFilter;
            while (h) {
                if (!c || (d = R.exec(h))) d && (h = h.slice(d[0].length) || h),
                i.push(f = []);
                c = !1;
                if (d = S.exec(h)) c = d.shift(),
                f.push({
                    value: c,
                    type: d[0].replace(Q, " ")
                }),
                h = h.slice(c.length);
                for (g in e.filter)(d = X[g].exec(h)) && (!j[g] || (d = j[g](d))) && (c = d.shift(), f.push({
                    value: c,
                    type: g,
                    matches: d
                }), h = h.slice(c.length));
                if (!c) break
            }
            return b ? h.length: h ? bi.error(a) : y(a, i).slice(0)
        }
        function bq(a) {
            var b = 0,
            c = a.length,
            d = "";
            for (; b < c; b++) d += a[b].value;
            return d
        }
        function br(a, b, c) {
            var e = b.dir,
            f = c && e === "parentNode",
            g = w++;
            return b.first ?
            function(b, c, d) {
                while (b = b[e]) if (b.nodeType === 1 || f) return a(b, c, d)
            }: function(b, c, h) {
                var i, j, k, l = v + " " + g;
                if (h) {
                    while (b = b[e]) if (b.nodeType === 1 || f) if (a(b, c, h)) return ! 0
                } else while (b = b[e]) if (b.nodeType === 1 || f) {
                    k = b[s] || (b[s] = {});
                    if ((j = k[e]) && j[0] === l) {
                        if ((i = j[1]) === !0 || i === d) return i === !0
                    } else {
                        j = k[e] = [l],
                        j[1] = a(b, c, h) || d;
                        if (j[1] === !0) return ! 0
                    }
                }
            }
        }
        function bs(a) {
            return a.length > 1 ?
            function(b, c, d) {
                var e = a.length;
                while (e--) if (!a[e](b, c, d)) return ! 1;
                return ! 0
            }: a[0]
        }
        function bt(a, b, c, d, e) {
            var f, g = [],
            h = 0,
            i = a.length,
            j = b != null;
            for (; h < i; h++) if (f = a[h]) if (!c || c(f, d, e)) g.push(f),
            j && b.push(h);
            return g
        }
        function bu(a, b, c, d, e, f) {
            return d && !d[s] && (d = bu(d)),
            e && !e[s] && (e = bu(e, f)),
            bg(function(f, g, h, i) {
                var j, k, l, m = [],
                n = [],
                o = g.length,
                p = f || bx(b || "*", h.nodeType ? [h] : h, []),
                q = a && (f || !b) ? bt(p, m, a, h, i) : p,
                r = c ? e || (f ? a: o || d) ? [] : g: q;
                c && c(q, r, h, i);
                if (d) {
                    j = bt(r, n),
                    d(j, [], h, i),
                    k = j.length;
                    while (k--) if (l = j[k]) r[n[k]] = !(q[n[k]] = l)
                }
                if (f) {
                    if (e || a) {
                        if (e) {
                            j = [],
                            k = r.length;
                            while (k--)(l = r[k]) && j.push(q[k] = l);
                            e(null, r = [], j, i)
                        }
                        k = r.length;
                        while (k--)(l = r[k]) && (j = e ? J.call(f, l) : m[k]) > -1 && (f[j] = !(g[j] = l))
                    }
                } else r = bt(r === g ? r.splice(o, r.length) : r),
                e ? e(null, g, r, i) : H.apply(g, r)
            })
        }
        function bv(a) {
            var b, c, d, f = a.length,
            g = e.relative[a[0].type],
            h = g || e.relative[" "],
            j = g ? 1 : 0,
            k = br(function(a) {
                return a === b
            },
            h, !0),
            l = br(function(a) {
                return J.call(b, a) > -1
            },
            h, !0),
            m = [function(a, c, d) {
                return ! g && (d || c !== i) || ((b = c).nodeType ? k(a, c, d) : l(a, c, d))
            }];
            for (; j < f; j++) if (c = e.relative[a[j].type]) m = [br(bs(m), c)];
            else {
                c = e.filter[a[j].type].apply(null, a[j].matches);
                if (c[s]) {
                    d = ++j;
                    for (; d < f; d++) if (e.relative[a[d].type]) break;
                    return bu(j > 1 && bs(m), j > 1 && bq(a.slice(0, j - 1)).replace(Q, "$1"), c, j < d && bv(a.slice(j, d)), d < f && bv(a = a.slice(d)), d < f && bq(a))
                }
                m.push(c)
            }
            return bs(m)
        }
        function bw(a, b) {
            var c = 0,
            f = b.length > 0,
            g = a.length > 0,
            h = function(h, j, k, m, n) {
                var o, p, q, r = [],
                s = 0,
                t = "0",
                u = h && [],
                w = n != null,
                x = i,
                y = h || g && e.find.TAG("*", n && j.parentNode || j),
                z = v += x == null ? 1 : Math.random() || .1;
                w && (i = j !== l && j, d = c);
                for (;
                (o = y[t]) != null; t++) {
                    if (g && o) {
                        p = 0;
                        while (q = a[p++]) if (q(o, j, k)) {
                            m.push(o);
                            break
                        }
                        w && (v = z, d = ++c)
                    }
                    f && ((o = !q && o) && s--, h && u.push(o))
                }
                s += t;
                if (f && t !== s) {
                    p = 0;
                    while (q = b[p++]) q(u, r, j, k);
                    if (h) {
                        if (s > 0) while (t--) ! u[t] && !r[t] && (r[t] = F.call(m));
                        r = bt(r)
                    }
                    H.apply(m, r),
                    w && !h && r.length > 0 && s + b.length > 1 && bi.uniqueSort(m)
                }
                return w && (v = z, i = x),
                u
            };
            return f ? bg(h) : h
        }
        function bx(a, b, c) {
            var d = 0,
            e = b.length;
            for (; d < e; d++) bi(a, b[d], c);
            return c
        }
        function by(a, b, c, d) {
            var f, g, i, j, k, l = bp(a);
            if (!d && l.length === 1) {
                g = l[0] = l[0].slice(0);
                if (g.length > 2 && (i = g[0]).type === "ID" && b.nodeType === 9 && n && e.relative[g[1].type]) {
                    b = (e.find.ID(i.matches[0].replace(bb, bc), b) || [])[0];
                    if (!b) return c;
                    a = a.slice(g.shift().value.length)
                }
                f = X.needsContext.test(a) ? 0 : g.length;
                while (f--) {
                    i = g[f];
                    if (e.relative[j = i.type]) break;
                    if (k = e.find[j]) if (d = k(i.matches[0].replace(bb, bc), T.test(g[0].type) && b.parentNode || b)) {
                        g.splice(f, 1),
                        a = d.length && bq(g);
                        if (!a) return H.apply(c, d),
                        c;
                        break
                    }
                }
            }
            return h(a, l)(d, b, !n, c, T.test(a)),
            c
        }
        function bz() {}
        var c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s = "sizzle" + -(new Date),
        t = a.document,
        u = {},
        v = 0,
        w = 0,
        x = bf(),
        y = bf(),
        z = bf(),
        A = !1,
        B = function() {
            return 0
        },
        C = typeof b,
        D = 1 << 31,
        E = [],
        F = E.pop,
        G = E.push,
        H = E.push,
        I = E.slice,
        J = E.indexOf ||
        function(a) {
            var b = 0,
            c = this.length;
            for (; b < c; b++) if (this[b] === a) return b;
            return - 1
        },
        K = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",
        L = "[\\x20\\t\\r\\n\\f]",
        M = "(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+",
        N = M.replace("w", "w#"),
        O = "\\[" + L + "*(" + M + ")" + L + "*(?:([*^$|!~]?=)" + L + "*(?:(['\"])((?:\\\\.|[^\\\\])*?)\\3|(" + N + ")|)|)" + L + "*\\]",
        P = ":(" + M + ")(?:\\(((['\"])((?:\\\\.|[^\\\\])*?)\\3|((?:\\\\.|[^\\\\()[\\]]|" + O.replace(3, 8) + ")*)|.*)\\)|)",
        Q = new RegExp("^" + L + "+|((?:^|[^\\\\])(?:\\\\.)*)" + L + "+$", "g"),
        R = new RegExp("^" + L + "*," + L + "*"),
        S = new RegExp("^" + L + "*([>+~]|" + L + ")" + L + "*"),
        T = new RegExp(L + "*[+~]"),
        U = new RegExp("=" + L + "*([^\\]'\"]*)" + L + "*\\]", "g"),
        V = new RegExp(P),
        W = new RegExp("^" + N + "$"),
        X = {
            ID: new RegExp("^#(" + M + ")"),
            CLASS: new RegExp("^\\.(" + M + ")"),
            TAG: new RegExp("^(" + M.replace("w", "w*") + ")"),
            ATTR: new RegExp("^" + O),
            PSEUDO: new RegExp("^" + P),
            CHILD: new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + L + "*(even|odd|(([+-]|)(\\d*)n|)" + L + "*(?:([+-]|)" + L + "*(\\d+)|))" + L + "*\\)|)", "i"),
            "boolean": new RegExp("^(?:" + K + ")$", "i"),
            needsContext: new RegExp("^" + L + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + L + "*((?:-\\d)?\\d*)" + L + "*\\)|)(?=[^-]|$)", "i")
        },
        Y = /^[^{]+\{\s*\[native \w/,
        Z = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,
        $ = /^(?:input|select|textarea|button)$/i,
        _ = /^h\d$/i,
        ba = /'|\\/g,
        bb = /\\([\da-fA-F]{1,6}[\x20\t\r\n\f]?|.)/g,
        bc = function(a, b) {
            var c = "0x" + b - 65536;
            return c !== c ? b: c < 0 ? String.fromCharCode(c + 65536) : String.fromCharCode(c >> 10 | 55296, c & 1023 | 56320)
        };
        try {
            H.apply(E = I.call(t.childNodes), t.childNodes),
            E[t.childNodes.length].nodeType
        } catch(bd) {
            H = {
                apply: E.length ?
                function(a, b) {
                    G.apply(a, I.call(b))
                }: function(a, b) {
                    var c = a.length,
                    d = 0;
                    while (a[c++] = b[d++]);
                    a.length = c - 1
                }
            }
        }
        g = bi.isXML = function(a) {
            var b = a && (a.ownerDocument || a).documentElement;
            return b ? b.nodeName !== "HTML": !1
        },
        k = bi.setDocument = function(a) {
            var c = a ? a.ownerDocument || a: t;
            if (c === l || c.nodeType !== 9 || !c.documentElement) return l;
            l = c,
            m = c.documentElement,
            n = !g(c),
            u.getElementsByTagName = bh(function(a) {
                return a.appendChild(c.createComment("")),
                !a.getElementsByTagName("*").length
            }),
            u.attributes = bh(function(a) {
                return a.className = "i",
                !a.getAttribute("className")
            }),
            u.getElementsByClassName = bh(function(a) {
                return a.innerHTML = "<div class='a'></div><div class='a i'></div>",
                a.firstChild.className = "i",
                a.getElementsByClassName("i").length === 2
            }),
            u.sortDetached = bh(function(a) {
                return a.compareDocumentPosition(l.createElement("div")) & 1
            }),
            u.getById = bh(function(a) {
                return m.appendChild(a).id = s,
                !c.getElementsByName || !c.getElementsByName(s).length
            }),
            u.getById ? (e.find.ID = function(a, b) {
                if (typeof b.getElementById !== C && n) {
                    var c = b.getElementById(a);
                    return c && c.parentNode ? [c] : []
                }
            },
            e.filter.ID = function(a) {
                var b = a.replace(bb, bc);
                return function(a) {
                    return a.getAttribute("id") === b
                }
            }) : (e.find.ID = function(a, c) {
                if (typeof c.getElementById !== C && n) {
                    var d = c.getElementById(a);
                    return d ? d.id === a || typeof d.getAttributeNode !== C && d.getAttributeNode("id").value === a ? [d] : b: []
                }
            },
            e.filter.ID = function(a) {
                var b = a.replace(bb, bc);
                return function(a) {
                    var c = typeof a.getAttributeNode !== C && a.getAttributeNode("id");
                    return c && c.value === b
                }
            }),
            e.find.TAG = u.getElementsByTagName ?
            function(a, b) {
                if (typeof b.getElementsByTagName !== C) return b.getElementsByTagName(a)
            }: function(a, b) {
                var c, d = [],
                e = 0,
                f = b.getElementsByTagName(a);
                if (a === "*") {
                    while (c = f[e++]) c.nodeType === 1 && d.push(c);
                    return d
                }
                return f
            },
            e.find.CLASS = u.getElementsByClassName &&
            function(a, b) {
                if (typeof b.getElementsByClassName !== C && n) return b.getElementsByClassName(a)
            },
            p = [],
            o = [];
            if (u.qsa = be(c.querySelectorAll)) bh(function(a) {
                a.innerHTML = "<select><option selected=''></option></select>",
                a.querySelectorAll("[selected]").length || o.push("\\[" + L + "*(?:value|" + K + ")"),
                a.querySelectorAll(":checked").length || o.push(":checked")
            }),
            bh(function(a) {
                var b = l.createElement("input");
                b.setAttribute("type", "hidden"),
                a.appendChild(b).setAttribute("t", ""),
                a.querySelectorAll("[t^='']").length && o.push("[*^$]=" + L + "*(?:''|\"\")"),
                a.querySelectorAll(":enabled").length || o.push(":enabled", ":disabled"),
                a.querySelectorAll("*,:x"),
                o.push(",.*:")
            });
            return (u.matchesSelector = be(q = m.webkitMatchesSelector || m.mozMatchesSelector || m.oMatchesSelector || m.msMatchesSelector)) && bh(function(a) {
                u.disconnectedMatch = q.call(a, "div"),
                q.call(a, "[s!='']:x"),
                p.push("!=", P)
            }),
            o = o.length && new RegExp(o.join("|")),
            p = p.length && new RegExp(p.join("|")),
            r = be(m.contains) || m.compareDocumentPosition ?
            function(a, b) {
                var c = a.nodeType === 9 ? a.documentElement: a,
                d = b && b.parentNode;
                return a === d || !!d && d.nodeType === 1 && !!(c.contains ? c.contains(d) : a.compareDocumentPosition && a.compareDocumentPosition(d) & 16)
            }: function(a, b) {
                if (b) while (b = b.parentNode) if (b === a) return ! 0;
                return ! 1
            },
            B = m.compareDocumentPosition ?
            function(a, b) {
                if (a === b) return A = !0,
                0;
                var d = b.compareDocumentPosition && a.compareDocumentPosition && a.compareDocumentPosition(b);
                if (d) return d & 1 || !u.sortDetached && b.compareDocumentPosition(a) === d ? a === c || r(t, a) ? -1 : b === c || r(t, b) ? 1 : j ? J.call(j, a) - J.call(j, b) : 0 : d & 4 ? -1 : 1;
                return a.compareDocumentPosition ? -1 : 1
            }: function(a, b) {
                var d, e = 0,
                f = a.parentNode,
                g = b.parentNode,
                h = [a],
                i = [b];
                if (a === b) return A = !0,
                0;
                if (!f || !g) return a === c ? -1 : b === c ? 1 : f ? -1 : g ? 1 : j ? J.call(j, a) - J.call(j, b) : 0;
                if (f === g) return bj(a, b);
                d = a;
                while (d = d.parentNode) h.unshift(d);
                d = b;
                while (d = d.parentNode) i.unshift(d);
                while (h[e] === i[e]) e++;
                return e ? bj(h[e], i[e]) : h[e] === t ? -1 : i[e] === t ? 1 : 0
            },
            l
        },
        bi.matches = function(a, b) {
            return bi(a, null, null, b)
        },
        bi.matchesSelector = function(a, b) { (a.ownerDocument || a) !== l && k(a),
            b = b.replace(U, "='$1']");
            if (u.matchesSelector && n && (!p || !p.test(b)) && (!o || !o.test(b))) try {
                var c = q.call(a, b);
                if (c || u.disconnectedMatch || a.document && a.document.nodeType !== 11) return c
            } catch(d) {}
            return bi(b, l, null, [a]).length > 0
        },
        bi.contains = function(a, b) {
            return (a.ownerDocument || a) !== l && k(a),
            r(a, b)
        },
        bi.attr = function(a, c) { (a.ownerDocument || a) !== l && k(a);
            var d = e.attrHandle[c.toLowerCase()],
            f = d && d(a, c, !n);
            return f === b ? u.attributes || !n ? a.getAttribute(c) : (f = a.getAttributeNode(c)) && f.specified ? f.value: null: f
        },
        bi.error = function(a) {
            throw new Error("Syntax error, unrecognized expression: " + a)
        },
        bi.uniqueSort = function(a) {
            var b, c = [],
            d = 0,
            e = 0;
            A = !u.detectDuplicates,
            j = !u.sortStable && a.slice(0),
            a.sort(B);
            if (A) {
                while (b = a[e++]) b === a[e] && (d = c.push(e));
                while (d--) a.splice(c[d], 1)
            }
            return a
        },
        f = bi.getText = function(a) {
            var b, c = "",
            d = 0,
            e = a.nodeType;
            if (!e) for (; b = a[d]; d++) c += f(b);
            else if (e === 1 || e === 9 || e === 11) {
                if (typeof a.textContent == "string") return a.textContent;
                for (a = a.firstChild; a; a = a.nextSibling) c += f(a)
            } else if (e === 3 || e === 4) return a.nodeValue;
            return c
        },
        e = bi.selectors = {
            cacheLength: 50,
            createPseudo: bg,
            match: X,
            attrHandle: {},
            find: {},
            relative: {
                ">": {
                    dir: "parentNode",
                    first: !0
                },
                " ": {
                    dir: "parentNode"
                },
                "+": {
                    dir: "previousSibling",
                    first: !0
                },
                "~": {
                    dir: "previousSibling"
                }
            },
            preFilter: {
                ATTR: function(a) {
                    return a[1] = a[1].replace(bb, bc),
                    a[3] = (a[4] || a[5] || "").replace(bb, bc),
                    a[2] === "~=" && (a[3] = " " + a[3] + " "),
                    a.slice(0, 4)
                },
                CHILD: function(a) {
                    return a[1] = a[1].toLowerCase(),
                    a[1].slice(0, 3) === "nth" ? (a[3] || bi.error(a[0]), a[4] = +(a[4] ? a[5] + (a[6] || 1) : 2 * (a[3] === "even" || a[3] === "odd")), a[5] = +(a[7] + a[8] || a[3] === "odd")) : a[3] && bi.error(a[0]),
                    a
                },
                PSEUDO: function(a) {
                    var b, c = !a[5] && a[2];
                    return X.CHILD.test(a[0]) ? null: (a[4] ? a[2] = a[4] : c && V.test(c) && (b = bp(c, !0)) && (b = c.indexOf(")", c.length - b) - c.length) && (a[0] = a[0].slice(0, b), a[2] = c.slice(0, b)), a.slice(0, 3))
                }
            },
            filter: {
                TAG: function(a) {
                    var b = a.replace(bb, bc).toLowerCase();
                    return a === "*" ?
                    function() {
                        return ! 0
                    }: function(a) {
                        return a.nodeName && a.nodeName.toLowerCase() === b
                    }
                },
                CLASS: function(a) {
                    var b = x[a + " "];
                    return b || (b = new RegExp("(^|" + L + ")" + a + "(" + L + "|$)")) && x(a,
                    function(a) {
                        return b.test(typeof a.className == "string" && a.className || typeof a.getAttribute !== C && a.getAttribute("class") || "")
                    })
                },
                ATTR: function(a, b, c) {
                    return function(d) {
                        var e = bi.attr(d, a);
                        return e == null ? b === "!=": b ? (e += "", b === "=" ? e === c: b === "!=" ? e !== c: b === "^=" ? c && e.indexOf(c) === 0 : b === "*=" ? c && e.indexOf(c) > -1 : b === "$=" ? c && e.slice( - c.length) === c: b === "~=" ? (" " + e + " ").indexOf(c) > -1 : b === "|=" ? e === c || e.slice(0, c.length + 1) === c + "-": !1) : !0
                    }
                },
                CHILD: function(a, b, c, d, e) {
                    var f = a.slice(0, 3) !== "nth",
                    g = a.slice( - 4) !== "last",
                    h = b === "of-type";
                    return d === 1 && e === 0 ?
                    function(a) {
                        return !! a.parentNode
                    }: function(b, c, i) {
                        var j, k, l, m, n, o, p = f !== g ? "nextSibling": "previousSibling",
                        q = b.parentNode,
                        r = h && b.nodeName.toLowerCase(),
                        t = !i && !h;
                        if (q) {
                            if (f) {
                                while (p) {
                                    l = b;
                                    while (l = l[p]) if (h ? l.nodeName.toLowerCase() === r: l.nodeType === 1) return ! 1;
                                    o = p = a === "only" && !o && "nextSibling"
                                }
                                return ! 0
                            }
                            o = [g ? q.firstChild: q.lastChild];
                            if (g && t) {
                                k = q[s] || (q[s] = {}),
                                j = k[a] || [],
                                n = j[0] === v && j[1],
                                m = j[0] === v && j[2],
                                l = n && q.childNodes[n];
                                while (l = ++n && l && l[p] || (m = n = 0) || o.pop()) if (l.nodeType === 1 && ++m && l === b) {
                                    k[a] = [v, n, m];
                                    break
                                }
                            } else if (t && (j = (b[s] || (b[s] = {}))[a]) && j[0] === v) m = j[1];
                            else while (l = ++n && l && l[p] || (m = n = 0) || o.pop()) if ((h ? l.nodeName.toLowerCase() === r: l.nodeType === 1) && ++m) {
                                t && ((l[s] || (l[s] = {}))[a] = [v, m]);
                                if (l === b) break
                            }
                            return m -= e,
                            m === d || m % d === 0 && m / d >= 0
                        }
                    }
                },
                PSEUDO: function(a, b) {
                    var c, d = e.pseudos[a] || e.setFilters[a.toLowerCase()] || bi.error("unsupported pseudo: " + a);
                    return d[s] ? d(b) : d.length > 1 ? (c = [a, a, "", b], e.setFilters.hasOwnProperty(a.toLowerCase()) ? bg(function(a, c) {
                        var e, f = d(a, b),
                        g = f.length;
                        while (g--) e = J.call(a, f[g]),
                        a[e] = !(c[e] = f[g])
                    }) : function(a) {
                        return d(a, 0, c)
                    }) : d
                }
            },
            pseudos: {
                not: bg(function(a) {
                    var b = [],
                    c = [],
                    d = h(a.replace(Q, "$1"));
                    return d[s] ? bg(function(a, b, c, e) {
                        var f, g = d(a, null, e, []),
                        h = a.length;
                        while (h--) if (f = g[h]) a[h] = !(b[h] = f)
                    }) : function(a, e, f) {
                        return b[0] = a,
                        d(b, null, f, c),
                        !c.pop()
                    }
                }),
                has: bg(function(a) {
                    return function(b) {
                        return bi(a, b).length > 0
                    }
                }),
                contains: bg(function(a) {
                    return function(b) {
                        return (b.textContent || b.innerText || f(b)).indexOf(a) > -1
                    }
                }),
                lang: bg(function(a) {
                    return W.test(a || "") || bi.error("unsupported lang: " + a),
                    a = a.replace(bb, bc).toLowerCase(),
                    function(b) {
                        var c;
                        do
                        if (c = n ? b.lang: b.getAttribute("xml:lang") || b.getAttribute("lang")) return c = c.toLowerCase(),
                        c === a || c.indexOf(a + "-") === 0;
                        while ((b = b.parentNode) && b.nodeType === 1);
                        return ! 1
                    }
                }),
                target: function(b) {
                    var c = a.location && a.location.hash;
                    return c && c.slice(1) === b.id
                },
                root: function(a) {
                    return a === m
                },
                focus: function(a) {
                    return a === l.activeElement && (!l.hasFocus || l.hasFocus()) && !!(a.type || a.href || ~a.tabIndex)
                },
                enabled: function(a) {
                    return a.disabled === !1
                },
                disabled: function(a) {
                    return a.disabled === !0
                },
                checked: function(a) {
                    var b = a.nodeName.toLowerCase();
                    return b === "input" && !!a.checked || b === "option" && !!a.selected
                },
                selected: function(a) {
                    return a.parentNode && a.parentNode.selectedIndex,
                    a.selected === !0
                },
                empty: function(a) {
                    for (a = a.firstChild; a; a = a.nextSibling) if (a.nodeName > "@" || a.nodeType === 3 || a.nodeType === 4) return ! 1;
                    return ! 0
                },
                parent: function(a) {
                    return ! e.pseudos.empty(a)
                },
                header: function(a) {
                    return _.test(a.nodeName)
                },
                input: function(a) {
                    return $.test(a.nodeName)
                },
                button: function(a) {
                    var b = a.nodeName.toLowerCase();
                    return b === "input" && a.type === "button" || b === "button"
                },
                text: function(a) {
                    var b;
                    return a.nodeName.toLowerCase() === "input" && a.type === "text" && ((b = a.getAttribute("type")) == null || b.toLowerCase() === a.type)
                },
                first: bo(function() {
                    return [0]
                }),
                last: bo(function(a, b) {
                    return [b - 1]
                }),
                eq: bo(function(a, b, c) {
                    return [c < 0 ? c + b: c]
                }),
                even: bo(function(a, b) {
                    var c = 0;
                    for (; c < b; c += 2) a.push(c);
                    return a
                }),
                odd: bo(function(a, b) {
                    var c = 1;
                    for (; c < b; c += 2) a.push(c);
                    return a
                }),
                lt: bo(function(a, b, c) {
                    var d = c < 0 ? c + b: c;
                    for (; --d >= 0;) a.push(d);
                    return a
                }),
                gt: bo(function(a, b, c) {
                    var d = c < 0 ? c + b: c;
                    for (; ++d < b;) a.push(d);
                    return a
                })
            }
        };
        for (c in {
            radio: !0,
            checkbox: !0,
            file: !0,
            password: !0,
            image: !0
        }) e.pseudos[c] = bm(c);
        for (c in {
            submit: !0,
            reset: !0
        }) e.pseudos[c] = bn(c);
        h = bi.compile = function(a, b) {
            var c, d = [],
            e = [],
            f = z[a + " "];
            if (!f) {
                b || (b = bp(a)),
                c = b.length;
                while (c--) f = bv(b[c]),
                f[s] ? d.push(f) : e.push(f);
                f = z(a, bw(e, d))
            }
            return f
        },
        e.pseudos.nth = e.pseudos.eq,
        bz.prototype = e.filters = e.pseudos,
        e.setFilters = new bz,
        u.sortStable = s.split("").sort(B).join("") === s,
        k(),
        [0, 0].sort(B),
        u.detectDuplicates = A,
        bh(function(a) {
            a.innerHTML = "<a href='#'></a>";
            if (a.firstChild.getAttribute("href") !== "#") {
                var b = "type|href|height|width".split("|"),
                c = b.length;
                while (c--) e.attrHandle[b[c]] = bl
            }
        }),
        bh(function(a) {
            if (a.getAttribute("disabled") != null) {
                var b = K.split("|"),
                c = b.length;
                while (c--) e.attrHandle[b[c]] = bk
            }
        }),
        jQuery.find = bi,
        jQuery.expr = bi.selectors,
        jQuery.expr[":"] = jQuery.expr.pseudos,
        jQuery.unique = bi.uniqueSort,
        jQuery.text = bi.getText,
        jQuery.isXMLDoc = bi.isXML,
        jQuery.contains = bi.contains
    } (window);
    var optionsCache = {};
    jQuery.Callbacks = function(a) {
        a = typeof a == "string" ? optionsCache[a] || createOptions(a) : jQuery.extend({},
        a);
        var b, c, d, e, f, g, h = [],
        i = !a.once && [],
        j = function(l) {
            b = a.memory && l,
            c = !0,
            g = e || 0,
            e = 0,
            f = h.length,
            d = !0;
            for (; h && g < f; g++) if (h[g].apply(l[0], l[1]) === !1 && a.stopOnFalse) {
                b = !1;
                break
            }
            d = !1,
            h && (i ? i.length && j(i.shift()) : b ? h = [] : k.disable())
        },
        k = {
            add: function() {
                if (h) {
                    var c = h.length;
                    (function g(b) {
                        jQuery.each(b,
                        function(b, c) {
                            var d = jQuery.type(c);
                            d === "function" ? (!a.unique || !k.has(c)) && h.push(c) : c && c.length && d !== "string" && g(c)
                        })
                    })(arguments),
                    d ? f = h.length: b && (e = c, j(b))
                }
                return this
            },
            remove: function() {
                return h && jQuery.each(arguments,
                function(a, b) {
                    var c;
                    while ((c = jQuery.inArray(b, h, c)) > -1) h.splice(c, 1),
                    d && (c <= f && f--, c <= g && g--)
                }),
                this
            },
            has: function(a) {
                return a ? jQuery.inArray(a, h) > -1 : !!h && !!h.length
            },
            empty: function() {
                return h = [],
                f = 0,
                this
            },
            disable: function() {
                return h = i = b = undefined,
                this
            },
            disabled: function() {
                return ! h
            },
            lock: function() {
                return i = undefined,
                b || k.disable(),
                this
            },
            locked: function() {
                return ! i
            },
            fireWith: function(a, b) {
                return b = b || [],
                b = [a, b.slice ? b.slice() : b],
                h && (!c || i) && (d ? i.push(b) : j(b)),
                this
            },
            fire: function() {
                return k.fireWith(this, arguments),
                this
            },
            fired: function() {
                return !! c
            }
        };
        return k
    },
    jQuery.extend({
        Deferred: function(a) {
            var b = [["resolve", "done", jQuery.Callbacks("once memory"), "resolved"], ["reject", "fail", jQuery.Callbacks("once memory"), "rejected"], ["notify", "progress", jQuery.Callbacks("memory")]],
            c = "pending",
            d = {
                state: function() {
                    return c
                },
                always: function() {
                    return e.done(arguments).fail(arguments),
                    this
                },
                then: function() {
                    var a = arguments;
                    return jQuery.Deferred(function(c) {
                        jQuery.each(b,
                        function(b, f) {
                            var g = f[0],
                            h = jQuery.isFunction(a[b]) && a[b];
                            e[f[1]](function() {
                                var a = h && h.apply(this, arguments);
                                a && jQuery.isFunction(a.promise) ? a.promise().done(c.resolve).fail(c.reject).progress(c.notify) : c[g + "With"](this === d ? c.promise() : this, h ? [a] : arguments)
                            })
                        }),
                        a = null
                    }).promise()
                },
                promise: function(a) {
                    return a != null ? jQuery.extend(a, d) : d
                }
            },
            e = {};
            return d.pipe = d.then,
            jQuery.each(b,
            function(a, f) {
                var g = f[2],
                h = f[3];
                d[f[1]] = g.add,
                h && g.add(function() {
                    c = h
                },
                b[a ^ 1][2].disable, b[2][2].lock),
                e[f[0]] = function() {
                    return e[f[0] + "With"](this === e ? d: this, arguments),
                    this
                },
                e[f[0] + "With"] = g.fireWith
            }),
            d.promise(e),
            a && a.call(e, e),
            e
        },
        when: function(a) {
            var b = 0,
            c = core_slice.call(arguments),
            d = c.length,
            e = d !== 1 || a && jQuery.isFunction(a.promise) ? d: 0,
            f = e === 1 ? a: jQuery.Deferred(),
            g = function(a, b, c) {
                return function(d) {
                    b[a] = this,
                    c[a] = arguments.length > 1 ? core_slice.call(arguments) : d,
                    c === h ? f.notifyWith(b, c) : --e || f.resolveWith(b, c)
                }
            },
            h,
            i,
            j;
            if (d > 1) {
                h = new Array(d),
                i = new Array(d),
                j = new Array(d);
                for (; b < d; b++) c[b] && jQuery.isFunction(c[b].promise) ? c[b].promise().done(g(b, j, c)).fail(f.reject).progress(g(b, i, h)) : --e
            }
            return e || f.resolveWith(j, c),
            f.promise()
        }
    }),
    jQuery.support = function(a) {
        var b = document.createElement("input"),
        c = document.createDocumentFragment(),
        d = document.createElement("div"),
        e = document.createElement("select"),
        f = e.appendChild(document.createElement("option"));
        return b.type ? (b.type = "checkbox", a.checkOn = b.value !== "", a.optSelected = f.selected, a.reliableMarginRight = !0, a.boxSizingReliable = !0, a.pixelPosition = !1, b.checked = !0, a.noCloneChecked = b.cloneNode(!0).checked, e.disabled = !0, a.optDisabled = !f.disabled, b = document.createElement("input"), b.value = "t", b.type = "radio", a.radioValue = b.value === "t", b.setAttribute("checked", "t"), b.setAttribute("name", "t"), c.appendChild(b), a.checkClone = c.cloneNode(!0).cloneNode(!0).lastChild.checked, a.focusinBubbles = "onfocusin" in window, d.style.backgroundClip = "content-box", d.cloneNode(!0).style.backgroundClip = "", a.clearCloneStyle = d.style.backgroundClip === "content-box", jQuery(function() {
            var b, c, e = "padding:0;margin:0;border:0;display:block;-webkit-box-sizing:content-box;-moz-box-sizing:content-box;box-sizing:content-box",
            f = document.getElementsByTagName("body")[0];
            if (!f) return;
            b = document.createElement("div"),
            b.style.cssText = "border:0;width:0;height:0;position:absolute;top:0;left:-9999px;margin-top:1px",
            f.appendChild(b).appendChild(d),
            d.innerHTML = "",
            d.style.cssText = "-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;padding:1px;border:1px;display:block;width:4px;margin-top:1%;position:absolute;top:1%",
            jQuery.swap(f, f.style.zoom != null ? {
                zoom: 1
            }: {},
            function() {
                a.boxSizing = d.offsetWidth === 4
            }),
            window.getComputedStyle && (a.pixelPosition = (window.getComputedStyle(d, null) || {}).top !== "1%", a.boxSizingReliable = (window.getComputedStyle(d, null) || {
                width: "4px"
            }).width === "4px", c = d.appendChild(document.createElement("div")), c.style.cssText = d.style.cssText = e, c.style.marginRight = c.style.width = "0", d.style.width = "1px", a.reliableMarginRight = !parseFloat((window.getComputedStyle(c, null) || {}).marginRight)),
            f.removeChild(b)
        }), a) : a
    } ({});
    var data_user, data_priv, rbrace = /(?:\{[\s\S]*\}|\[[\s\S]*\])$/,
    rmultiDash = /([A-Z])/g;
    Data.uid = 1,
    Data.accepts = function(a) {
        return a.nodeType ? a.nodeType === 1 || a.nodeType === 9 : !0
    },
    Data.prototype = {
        key: function(a) {
            if (!Data.accepts(a)) return 0;
            var b = {},
            c = a[this.expando];
            if (!c) {
                c = Data.uid++;
                try {
                    b[this.expando] = {
                        value: c
                    },
                    Object.defineProperties(a, b)
                } catch(d) {
                    b[this.expando] = c,
                    jQuery.extend(a, b)
                }
            }
            return this.cache[c] || (this.cache[c] = {}),
            c
        },
        set: function(a, b, c) {
            var d, e = this.key(a),
            f = this.cache[e];
            if (typeof b == "string") f[b] = c;
            else if (jQuery.isEmptyObject(f)) this.cache[e] = b;
            else for (d in b) f[d] = b[d]
        },
        get: function(a, b) {
            var c = this.cache[this.key(a)];
            return b === undefined ? c: c[b]
        },
        access: function(a, b, c) {
            return b === undefined || b && typeof b == "string" && c === undefined ? this.get(a, b) : (this.set(a, b, c), c !== undefined ? c: b)
        },
        remove: function(a, b) {
            var c, d, e = this.key(a),
            f = this.cache[e];
            if (b === undefined) this.cache[e] = {};
            else {
                jQuery.isArray(b) ? d = b.concat(b.map(jQuery.camelCase)) : b in f ? d = [b] : (d = jQuery.camelCase(b), d = d in f ? [d] : d.match(core_rnotwhite) || []),
                c = d.length;
                while (c--) delete f[d[c]]
            }
        },
        hasData: function(a) {
            return ! jQuery.isEmptyObject(this.cache[a[this.expando]] || {})
        },
        discard: function(a) {
            delete this.cache[this.key(a)]
        }
    },
    data_user = new Data,
    data_priv = new Data,
    jQuery.extend({
        acceptData: Data.accepts,
        hasData: function(a) {
            return data_user.hasData(a) || data_priv.hasData(a)
        },
        data: function(a, b, c) {
            return data_user.access(a, b, c)
        },
        removeData: function(a, b) {
            data_user.remove(a, b)
        },
        _data: function(a, b, c) {
            return data_priv.access(a, b, c)
        },
        _removeData: function(a, b) {
            data_priv.remove(a, b)
        }
    }),
    jQuery.fn.extend({
        data: function(a, b) {
            var c, d, e = this[0],
            f = 0,
            g = null;
            if (a === undefined) {
                if (this.length) {
                    g = data_user.get(e);
                    if (e.nodeType === 1 && !data_priv.get(e, "hasDataAttrs")) {
                        c = e.attributes;
                        for (; f < c.length; f++) d = c[f].name,
                        d.indexOf("data-") === 0 && (d = jQuery.camelCase(d.substring(5)), dataAttr(e, d, g[d]));
                        data_priv.set(e, "hasDataAttrs", !0)
                    }
                }
                return g
            }
            return typeof a == "object" ? this.each(function() {
                data_user.set(this, a)
            }) : jQuery.access(this,
            function(b) {
                var c, d = jQuery.camelCase(a);
                if (e && b === undefined) {
                    c = data_user.get(e, a);
                    if (c !== undefined) return c;
                    c = data_user.get(e, d);
                    if (c !== undefined) return c;
                    c = dataAttr(e, d, undefined);
                    if (c !== undefined) return c;
                    return
                }
                this.each(function() {
                    var c = data_user.get(this, d);
                    data_user.set(this, d, b),
                    a.indexOf("-") !== -1 && c !== undefined && data_user.set(this, a, b)
                })
            },
            null, b, arguments.length > 1, null, !0)
        },
        removeData: function(a) {
            return this.each(function() {
                data_user.remove(this, a)
            })
        }
    }),
    jQuery.extend({
        queue: function(a, b, c) {
            var d;
            if (a) return b = (b || "fx") + "queue",
            d = data_priv.get(a, b),
            c && (!d || jQuery.isArray(c) ? d = data_priv.access(a, b, jQuery.makeArray(c)) : d.push(c)),
            d || []
        },
        dequeue: function(a, b) {
            b = b || "fx";
            var c = jQuery.queue(a, b),
            d = c.length,
            e = c.shift(),
            f = jQuery._queueHooks(a, b),
            g = function() {
                jQuery.dequeue(a, b)
            };
            e === "inprogress" && (e = c.shift(), d--),
            f.cur = e,
            e && (b === "fx" && c.unshift("inprogress"), delete f.stop, e.call(a, g, f)),
            !d && f && f.empty.fire()
        },
        _queueHooks: function(a, b) {
            var c = b + "queueHooks";
            return data_priv.get(a, c) || data_priv.access(a, c, {
                empty: jQuery.Callbacks("once memory").add(function() {
                    data_priv.remove(a, [b + "queue", c])
                })
            })
        }
    }),
    jQuery.fn.extend({
        queue: function(a, b) {
            var c = 2;
            return typeof a != "string" && (b = a, a = "fx", c--),
            arguments.length < c ? jQuery.queue(this[0], a) : b === undefined ? this: this.each(function() {
                var c = jQuery.queue(this, a, b);
                jQuery._queueHooks(this, a),
                a === "fx" && c[0] !== "inprogress" && jQuery.dequeue(this, a)
            })
        },
        dequeue: function(a) {
            return this.each(function() {
                jQuery.dequeue(this, a)
            })
        },
        delay: function(a, b) {
            return a = jQuery.fx ? jQuery.fx.speeds[a] || a: a,
            b = b || "fx",
            this.queue(b,
            function(b, c) {
                var d = setTimeout(b, a);
                c.stop = function() {
                    clearTimeout(d)
                }
            })
        },
        clearQueue: function(a) {
            return this.queue(a || "fx", [])
        },
        promise: function(a, b) {
            var c, d = 1,
            e = jQuery.Deferred(),
            f = this,
            g = this.length,
            h = function() {--d || e.resolveWith(f, [f])
            };
            typeof a != "string" && (b = a, a = undefined),
            a = a || "fx";
            while (g--) c = data_priv.get(f[g], a + "queueHooks"),
            c && c.empty && (d++, c.empty.add(h));
            return h(),
            e.promise(b)
        }
    });
    var nodeHook, boolHook, rclass = /[\t\r\n]/g,
    rreturn = /\r/g,
    rfocusable = /^(?:input|select|textarea|button)$/i;
    jQuery.fn.extend({
        attr: function(a, b) {
            return jQuery.access(this, jQuery.attr, a, b, arguments.length > 1)
        },
        removeAttr: function(a) {
            return this.each(function() {
                jQuery.removeAttr(this, a)
            })
        },
        prop: function(a, b) {
            return jQuery.access(this, jQuery.prop, a, b, arguments.length > 1)
        },
        removeProp: function(a) {
            return this.each(function() {
                delete this[jQuery.propFix[a] || a]
            })
        },
        addClass: function(a) {
            var b, c, d, e, f, g = 0,
            h = this.length,
            i = typeof a == "string" && a;
            if (jQuery.isFunction(a)) return this.each(function(b) {
                jQuery(this).addClass(a.call(this, b, this.className))
            });
            if (i) {
                b = (a || "").match(core_rnotwhite) || [];
                for (; g < h; g++) {
                    c = this[g],
                    d = c.nodeType === 1 && (c.className ? (" " + c.className + " ").replace(rclass, " ") : " ");
                    if (d) {
                        f = 0;
                        while (e = b[f++]) d.indexOf(" " + e + " ") < 0 && (d += e + " ");
                        c.className = jQuery.trim(d)
                    }
                }
            }
            return this
        },
        removeClass: function(a) {
            var b, c, d, e, f, g = 0,
            h = this.length,
            i = arguments.length === 0 || typeof a == "string" && a;
            if (jQuery.isFunction(a)) return this.each(function(b) {
                jQuery(this).removeClass(a.call(this, b, this.className))
            });
            if (i) {
                b = (a || "").match(core_rnotwhite) || [];
                for (; g < h; g++) {
                    c = this[g],
                    d = c.nodeType === 1 && (c.className ? (" " + c.className + " ").replace(rclass, " ") : "");
                    if (d) {
                        f = 0;
                        while (e = b[f++]) while (d.indexOf(" " + e + " ") >= 0) d = d.replace(" " + e + " ", " ");
                        c.className = a ? jQuery.trim(d) : ""
                    }
                }
            }
            return this
        },
        toggleClass: function(a, b) {
            var c = typeof a,
            d = typeof b == "boolean";
            return jQuery.isFunction(a) ? this.each(function(c) {
                jQuery(this).toggleClass(a.call(this, c, this.className, b), b)
            }) : this.each(function() {
                if (c === "string") {
                    var e, f = 0,
                    g = jQuery(this),
                    h = b,
                    i = a.match(core_rnotwhite) || [];
                    while (e = i[f++]) h = d ? h: !g.hasClass(e),
                    g[h ? "addClass": "removeClass"](e)
                } else if (c === core_strundefined || c === "boolean") this.className && data_priv.set(this, "__className__", this.className),
                this.className = this.className || a === !1 ? "": data_priv.get(this, "__className__") || ""
            })
        },
        hasClass: function(a) {
            var b = " " + a + " ",
            c = 0,
            d = this.length;
            for (; c < d; c++) if (this[c].nodeType === 1 && (" " + this[c].className + " ").replace(rclass, " ").indexOf(b) >= 0) return ! 0;
            return ! 1
        },
        val: function(a) {
            var b, c, d, e = this[0];
            if (!arguments.length) {
                if (e) return b = jQuery.valHooks[e.type] || jQuery.valHooks[e.nodeName.toLowerCase()],
                b && "get" in b && (c = b.get(e, "value")) !== undefined ? c: (c = e.value, typeof c == "string" ? c.replace(rreturn, "") : c == null ? "": c);
                return
            }
            return d = jQuery.isFunction(a),
            this.each(function(c) {
                var e, f = jQuery(this);
                if (this.nodeType !== 1) return;
                d ? e = a.call(this, c, f.val()) : e = a,
                e == null ? e = "": typeof e == "number" ? e += "": jQuery.isArray(e) && (e = jQuery.map(e,
                function(a) {
                    return a == null ? "": a + ""
                })),
                b = jQuery.valHooks[this.type] || jQuery.valHooks[this.nodeName.toLowerCase()];
                if (!b || !("set" in b) || b.set(this, e, "value") === undefined) this.value = e
            })
        }
    }),
    jQuery.extend({
        valHooks: {
            option: {
                get: function(a) {
                    var b = a.attributes.value;
                    return ! b || b.specified ? a.value: a.text
                }
            },
            select: {
                get: function(a) {
                    var b, c, d = a.options,
                    e = a.selectedIndex,
                    f = a.type === "select-one" || e < 0,
                    g = f ? null: [],
                    h = f ? e + 1 : d.length,
                    i = e < 0 ? h: f ? e: 0;
                    for (; i < h; i++) {
                        c = d[i];
                        if ((c.selected || i === e) && (jQuery.support.optDisabled ? !c.disabled: c.getAttribute("disabled") === null) && (!c.parentNode.disabled || !jQuery.nodeName(c.parentNode, "optgroup"))) {
                            b = jQuery(c).val();
                            if (f) return b;
                            g.push(b)
                        }
                    }
                    return g
                },
                set: function(a, b) {
                    var c, d, e = a.options,
                    f = jQuery.makeArray(b),
                    g = e.length;
                    while (g--) {
                        d = e[g];
                        if (d.selected = jQuery.inArray(jQuery(d).val(), f) >= 0) c = !0
                    }
                    return c || (a.selectedIndex = -1),
                    f
                }
            }
        },
        attr: function(a, b, c) {
            var d, e, f = a.nodeType;
            if (!a || f === 3 || f === 8 || f === 2) return;
            if (typeof a.getAttribute === core_strundefined) return jQuery.prop(a, b, c);
            if (f !== 1 || !jQuery.isXMLDoc(a)) b = b.toLowerCase(),
            d = jQuery.attrHooks[b] || (jQuery.expr.match.boolean.test(b) ? boolHook: nodeHook);
            if (c === undefined) return d && "get" in d && (e = d.get(a, b)) !== null ? e: (e = jQuery.find.attr(a, b), e == null ? undefined: e);
            if (c === null) jQuery.removeAttr(a, b);
            else return d && "set" in d && (e = d.set(a, c, b)) !== undefined ? e: (a.setAttribute(b, c + ""), c)
        },
        removeAttr: function(a, b) {
            var c, d, e = 0,
            f = b && b.match(core_rnotwhite);
            if (f && a.nodeType === 1) while (c = f[e++]) d = jQuery.propFix[c] || c,
            jQuery.expr.match.boolean.test(c) && (a[d] = !1),
            a.removeAttribute(c)
        },
        attrHooks: {
            type: {
                set: function(a, b) {
                    if (!jQuery.support.radioValue && b === "radio" && jQuery.nodeName(a, "input")) {
                        var c = a.value;
                        return a.setAttribute("type", b),
                        c && (a.value = c),
                        b
                    }
                }
            }
        },
        propFix: {
            "for": "htmlFor",
            "class": "className"
        },
        prop: function(a, b, c) {
            var d, e, f, g = a.nodeType;
            if (!a || g === 3 || g === 8 || g === 2) return;
            return f = g !== 1 || !jQuery.isXMLDoc(a),
            f && (b = jQuery.propFix[b] || b, e = jQuery.propHooks[b]),
            c !== undefined ? e && "set" in e && (d = e.set(a, c, b)) !== undefined ? d: a[b] = c: e && "get" in e && (d = e.get(a, b)) !== null ? d: a[b]
        },
        propHooks: {
            tabIndex: {
                get: function(a) {
                    return a.hasAttribute("tabindex") || rfocusable.test(a.nodeName) || a.href ? a.tabIndex: -1
                }
            }
        }
    }),
    boolHook = {
        set: function(a, b, c) {
            return b === !1 ? jQuery.removeAttr(a, c) : a.setAttribute(c, c),
            c
        }
    },
    jQuery.each(jQuery.expr.match.boolean.source.match(/\w+/g),
    function(a, b) {
        var c = jQuery.expr.attrHandle[b] || jQuery.find.attr;
        jQuery.expr.attrHandle[b] = function(a, b, d) {
            var e = jQuery.expr.attrHandle[b],
            f = d ? undefined: (jQuery.expr.attrHandle[b] = undefined) != c(a, b, d) ? b.toLowerCase() : null;
            return jQuery.expr.attrHandle[b] = e,
            f
        }
    }),
    jQuery.support.optSelected || (jQuery.propHooks.selected = {
        get: function(a) {
            var b = a.parentNode;
            return b && b.parentNode && b.parentNode.selectedIndex,
            null
        }
    }),
    jQuery.each(["tabIndex", "readOnly", "maxLength", "cellSpacing", "cellPadding", "rowSpan", "colSpan", "useMap", "frameBorder", "contentEditable"],
    function() {
        jQuery.propFix[this.toLowerCase()] = this
    }),
    jQuery.each(["radio", "checkbox"],
    function() {
        jQuery.valHooks[this] = {
            set: function(a, b) {
                if (jQuery.isArray(b)) return a.checked = jQuery.inArray(jQuery(a).val(), b) >= 0
            }
        },
        jQuery.support.checkOn || (jQuery.valHooks[this].get = function(a) {
            return a.getAttribute("value") === null ? "on": a.value
        })
    });
    var rkeyEvent = /^key/,
    rmouseEvent = /^(?:mouse|contextmenu)|click/,
    rfocusMorph = /^(?:focusinfocus|focusoutblur)$/,
    rtypenamespace = /^([^.]*)(?:\.(.+)|)$/;
    jQuery.event = {
        global: {},
        add: function(a, b, c, d, e) {
            var f, g, h, i, j, k, l, m, n, o, p, q = data_priv.get(a);
            if (!q) return;
            c.handler && (f = c, c = f.handler, e = f.selector),
            c.guid || (c.guid = jQuery.guid++),
            (i = q.events) || (i = q.events = {}),
            (g = q.handle) || (g = q.handle = function(a) {
                return typeof jQuery === core_strundefined || !!a && jQuery.event.triggered === a.type ? undefined: jQuery.event.dispatch.apply(g.elem, arguments)
            },
            g.elem = a),
            b = (b || "").match(core_rnotwhite) || [""],
            j = b.length;
            while (j--) {
                h = rtypenamespace.exec(b[j]) || [],
                n = p = h[1],
                o = (h[2] || "").split(".").sort();
                if (!n) continue;
                l = jQuery.event.special[n] || {},
                n = (e ? l.delegateType: l.bindType) || n,
                l = jQuery.event.special[n] || {},
                k = jQuery.extend({
                    type: n,
                    origType: p,
                    data: d,
                    handler: c,
                    guid: c.guid,
                    selector: e,
                    needsContext: e && jQuery.expr.match.needsContext.test(e),
                    namespace: o.join(".")
                },
                f),
                (m = i[n]) || (m = i[n] = [], m.delegateCount = 0, (!l.setup || l.setup.call(a, d, o, g) === !1) && a.addEventListener && a.addEventListener(n, g, !1)),
                l.add && (l.add.call(a, k), k.handler.guid || (k.handler.guid = c.guid)),
                e ? m.splice(m.delegateCount++, 0, k) : m.push(k),
                jQuery.event.global[n] = !0
            }
            a = null
        },
        remove: function(a, b, c, d, e) {
            var f, g, h, i, j, k, l, m, n, o, p, q = data_priv.hasData(a) && data_priv.get(a);
            if (!q || !(i = q.events)) return;
            b = (b || "").match(core_rnotwhite) || [""],
            j = b.length;
            while (j--) {
                h = rtypenamespace.exec(b[j]) || [],
                n = p = h[1],
                o = (h[2] || "").split(".").sort();
                if (!n) {
                    for (n in i) jQuery.event.remove(a, n + b[j], c, d, !0);
                    continue
                }
                l = jQuery.event.special[n] || {},
                n = (d ? l.delegateType: l.bindType) || n,
                m = i[n] || [],
                h = h[2] && new RegExp("(^|\\.)" + o.join("\\.(?:.*\\.|)") + "(\\.|$)"),
                g = f = m.length;
                while (f--) k = m[f],
                (e || p === k.origType) && (!c || c.guid === k.guid) && (!h || h.test(k.namespace)) && (!d || d === k.selector || d === "**" && k.selector) && (m.splice(f, 1), k.selector && m.delegateCount--, l.remove && l.remove.call(a, k));
                g && !m.length && ((!l.teardown || l.teardown.call(a, o, q.handle) === !1) && jQuery.removeEvent(a, n, q.handle), delete i[n])
            }
            jQuery.isEmptyObject(i) && (delete q.handle, data_priv.remove(a, "events"))
        },
        trigger: function(a, b, c, d) {
            var e, f, g, h, i, j, k, l = [c || document],
            m = core_hasOwn.call(a, "type") ? a.type: a,
            n = core_hasOwn.call(a, "namespace") ? a.namespace.split(".") : [];
            f = g = c = c || document;
            if (c.nodeType === 3 || c.nodeType === 8) return;
            if (rfocusMorph.test(m + jQuery.event.triggered)) return;
            m.indexOf(".") >= 0 && (n = m.split("."), m = n.shift(), n.sort()),
            i = m.indexOf(":") < 0 && "on" + m,
            a = a[jQuery.expando] ? a: new jQuery.Event(m, typeof a == "object" && a),
            a.isTrigger = d ? 2 : 3,
            a.namespace = n.join("."),
            a.namespace_re = a.namespace ? new RegExp("(^|\\.)" + n.join("\\.(?:.*\\.|)") + "(\\.|$)") : null,
            a.result = undefined,
            a.target || (a.target = c),
            b = b == null ? [a] : jQuery.makeArray(b, [a]),
            k = jQuery.event.special[m] || {};
            if (!d && k.trigger && k.trigger.apply(c, b) === !1) return;
            if (!d && !k.noBubble && !jQuery.isWindow(c)) {
                h = k.delegateType || m,
                rfocusMorph.test(h + m) || (f = f.parentNode);
                for (; f; f = f.parentNode) l.push(f),
                g = f;
                g === (c.ownerDocument || document) && l.push(g.defaultView || g.parentWindow || window)
            }
            e = 0;
            while ((f = l[e++]) && !a.isPropagationStopped()) a.type = e > 1 ? h: k.bindType || m,
            j = (data_priv.get(f, "events") || {})[a.type] && data_priv.get(f, "handle"),
            j && j.apply(f, b),
            j = i && f[i],
            j && jQuery.acceptData(f) && j.apply && j.apply(f, b) === !1 && a.preventDefault();
            return a.type = m,
            !d && !a.isDefaultPrevented() && (!k._default || k._default.apply(l.pop(), b) === !1) && jQuery.acceptData(c) && i && jQuery.isFunction(c[m]) && !jQuery.isWindow(c) && (g = c[i], g && (c[i] = null), jQuery.event.triggered = m, c[m](), jQuery.event.triggered = undefined, g && (c[i] = g)),
            a.result
        },
        dispatch: function(a) {
            a = jQuery.event.fix(a);
            var b, c, d, e, f, g = [],
            h = core_slice.call(arguments),
            i = (data_priv.get(this, "events") || {})[a.type] || [],
            j = jQuery.event.special[a.type] || {};
            h[0] = a,
            a.delegateTarget = this;
            if (j.preDispatch && j.preDispatch.call(this, a) === !1) return;
            g = jQuery.event.handlers.call(this, a, i),
            b = 0;
            while ((e = g[b++]) && !a.isPropagationStopped()) {
                a.currentTarget = e.elem,
                c = 0;
                while ((f = e.handlers[c++]) && !a.isImmediatePropagationStopped()) if (!a.namespace_re || a.namespace_re.test(f.namespace)) a.handleObj = f,
                a.data = f.data,
                d = ((jQuery.event.special[f.origType] || {}).handle || f.handler).apply(e.elem, h),
                d !== undefined && (a.result = d) === !1 && (a.preventDefault(), a.stopPropagation())
            }
            return j.postDispatch && j.postDispatch.call(this, a),
            a.result
        },
        handlers: function(a, b) {
            var c, d, e, f, g = [],
            h = b.delegateCount,
            i = a.target;
            if (h && i.nodeType && (!a.button || a.type !== "click")) for (; i !== this; i = i.parentNode || this) if (i.disabled !== !0 || a.type !== "click") {
                d = [];
                for (c = 0; c < h; c++) f = b[c],
                e = f.selector + " ",
                d[e] === undefined && (d[e] = f.needsContext ? jQuery(e, this).index(i) >= 0 : jQuery.find(e, this, null, [i]).length),
                d[e] && d.push(f);
                d.length && g.push({
                    elem: i,
                    handlers: d
                })
            }
            return h < b.length && g.push({
                elem: this,
                handlers: b.slice(h)
            }),
            g
        },
        props: "altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),
        fixHooks: {},
        keyHooks: {
            props: "char charCode key keyCode".split(" "),
            filter: function(a, b) {
                return a.which == null && (a.which = b.charCode != null ? b.charCode: b.keyCode),
                a
            }
        },
        mouseHooks: {
            props: "button buttons clientX clientY offsetX offsetY pageX pageY screenX screenY toElement".split(" "),
            filter: function(a, b) {
                var c, d, e, f = b.button;
                return a.pageX == null && b.clientX != null && (c = a.target.ownerDocument || document, d = c.documentElement, e = c.body, a.pageX = b.clientX + (d && d.scrollLeft || e && e.scrollLeft || 0) - (d && d.clientLeft || e && e.clientLeft || 0), a.pageY = b.clientY + (d && d.scrollTop || e && e.scrollTop || 0) - (d && d.clientTop || e && e.clientTop || 0)),
                !a.which && f !== undefined && (a.which = f & 1 ? 1 : f & 2 ? 3 : f & 4 ? 2 : 0),
                a
            }
        },
        fix: function(a) {
            if (a[jQuery.expando]) return a;
            var b, c, d, e = a.type,
            f = a,
            g = this.fixHooks[e];
            g || (this.fixHooks[e] = g = rmouseEvent.test(e) ? this.mouseHooks: rkeyEvent.test(e) ? this.keyHooks: {}),
            d = g.props ? this.props.concat(g.props) : this.props,
            a = new jQuery.Event(f),
            b = d.length;
            while (b--) c = d[b],
            a[c] = f[c];
            return a.target.nodeType === 3 && (a.target = a.target.parentNode),
            g.filter ? g.filter(a, f) : a
        },
        special: {
            load: {
                noBubble: !0
            },
            focus: {
                trigger: function() {
                    if (this !== safeActiveElement() && this.focus) return this.focus(),
                    !1
                },
                delegateType: "focusin"
            },
            blur: {
                trigger: function() {
                    if (this === safeActiveElement() && this.blur) return this.blur(),
                    !1
                },
                delegateType: "focusout"
            },
            click: {
                trigger: function() {
                    if (this.type === "checkbox" && this.click && jQuery.nodeName(this, "input")) return this.click(),
                    !1
                },
                _default: function(a) {
                    return jQuery.nodeName(a.target, "a")
                }
            },
            beforeunload: {
                postDispatch: function(a) {
                    a.result !== undefined && (a.originalEvent.returnValue = a.result)
                }
            }
        },
        simulate: function(a, b, c, d) {
            var e = jQuery.extend(new jQuery.Event, c, {
                type: a,
                isSimulated: !0,
                originalEvent: {}
            });
            d ? jQuery.event.trigger(e, null, b) : jQuery.event.dispatch.call(b, e),
            e.isDefaultPrevented() && c.preventDefault()
        }
    },
    jQuery.removeEvent = function(a, b, c) {
        a.removeEventListener && a.removeEventListener(b, c, !1)
    },
    jQuery.Event = function(a, b) {
        if (this instanceof jQuery.Event) a && a.type ? (this.originalEvent = a, this.type = a.type, this.isDefaultPrevented = a.defaultPrevented || a.getPreventDefault && a.getPreventDefault() ? returnTrue: returnFalse) : this.type = a,
        b && jQuery.extend(this, b),
        this.timeStamp = a && a.timeStamp || jQuery.now(),
        this[jQuery.expando] = !0;
        else return new jQuery.Event(a, b)
    },
    jQuery.Event.prototype = {
        isDefaultPrevented: returnFalse,
        isPropagationStopped: returnFalse,
        isImmediatePropagationStopped: returnFalse,
        preventDefault: function() {
            var a = this.originalEvent;
            this.isDefaultPrevented = returnTrue,
            a && a.preventDefault && a.preventDefault()
        },
        stopPropagation: function() {
            var a = this.originalEvent;
            this.isPropagationStopped = returnTrue,
            a && a.stopPropagation && a.stopPropagation()
        },
        stopImmediatePropagation: function() {
            this.isImmediatePropagationStopped = returnTrue,
            this.stopPropagation()
        }
    },
    jQuery.each({
        mouseenter: "mouseover",
        mouseleave: "mouseout"
    },
    function(a, b) {
        jQuery.event.special[a] = {
            delegateType: b,
            bindType: b,
            handle: function(a) {
                var c, d = this,
                e = a.relatedTarget,
                f = a.handleObj;
                if (!e || e !== d && !jQuery.contains(d, e)) a.type = f.origType,
                c = f.handler.apply(this, arguments),
                a.type = b;
                return c
            }
        }
    }),
    jQuery.support.focusinBubbles || jQuery.each({
        focus: "focusin",
        blur: "focusout"
    },
    function(a, b) {
        var c = 0,
        d = function(a) {
            jQuery.event.simulate(b, a.target, jQuery.event.fix(a), !0)
        };
        jQuery.event.special[b] = {
            setup: function() {
                c++===0 && document.addEventListener(a, d, !0)
            },
            teardown: function() {--c === 0 && document.removeEventListener(a, d, !0)
            }
        }
    }),
    jQuery.fn.extend({
        on: function(a, b, c, d, e) {
            var f, g;
            if (typeof a == "object") {
                typeof b != "string" && (c = c || b, b = undefined);
                for (g in a) this.on(g, b, c, a[g], e);
                return this
            }
            c == null && d == null ? (d = b, c = b = undefined) : d == null && (typeof b == "string" ? (d = c, c = undefined) : (d = c, c = b, b = undefined));
            if (d === !1) d = returnFalse;
            else if (!d) return this;
            return e === 1 && (f = d, d = function(a) {
                return jQuery().off(a),
                f.apply(this, arguments)
            },
            d.guid = f.guid || (f.guid = jQuery.guid++)),
            this.each(function() {
                jQuery.event.add(this, a, d, c, b)
            })
        },
        one: function(a, b, c, d) {
            return this.on(a, b, c, d, 1)
        },
        off: function(a, b, c) {
            var d, e;
            if (a && a.preventDefault && a.handleObj) return d = a.handleObj,
            jQuery(a.delegateTarget).off(d.namespace ? d.origType + "." + d.namespace: d.origType, d.selector, d.handler),
            this;
            if (typeof a == "object") {
                for (e in a) this.off(e, b, a[e]);
                return this
            }
            if (b === !1 || typeof b == "function") c = b,
            b = undefined;
            return c === !1 && (c = returnFalse),
            this.each(function() {
                jQuery.event.remove(this, a, c, b)
            })
        },
        trigger: function(a, b) {
            return this.each(function() {
                jQuery.event.trigger(a, b, this)
            })
        },
        triggerHandler: function(a, b) {
            var c = this[0];
            if (c) return jQuery.event.trigger(a, b, c, !0)
        }
    });
    var isSimple = /^.[^:#\[\.,]*$/,
    rneedsContext = jQuery.expr.match.needsContext,
    guaranteedUnique = {
        children: !0,
        contents: !0,
        next: !0,
        prev: !0
    };
    jQuery.fn.extend({
        find: function(a) {
            var b, c, d, e = this.length;
            if (typeof a != "string") return b = this,
            this.pushStack(jQuery(a).filter(function() {
                for (d = 0; d < e; d++) if (jQuery.contains(b[d], this)) return ! 0
            }));
            c = [];
            for (d = 0; d < e; d++) jQuery.find(a, this[d], c);
            return c = this.pushStack(e > 1 ? jQuery.unique(c) : c),
            c.selector = (this.selector ? this.selector + " ": "") + a,
            c
        },
        has: function(a) {
            var b = jQuery(a, this),
            c = b.length;
            return this.filter(function() {
                var a = 0;
                for (; a < c; a++) if (jQuery.contains(this, b[a])) return ! 0
            })
        },
        not: function(a) {
            return this.pushStack(winnow(this, a || [], !0))
        },
        filter: function(a) {
            return this.pushStack(winnow(this, a || [], !1))
        },
        is: function(a) {
            return !! a && (typeof a == "string" ? rneedsContext.test(a) ? jQuery(a, this.context).index(this[0]) >= 0 : jQuery.filter(a, this).length > 0 : this.filter(a).length > 0)
        },
        closest: function(a, b) {
            var c, d = 0,
            e = this.length,
            f = [],
            g = rneedsContext.test(a) || typeof a != "string" ? jQuery(a, b || this.context) : 0;
            for (; d < e; d++) for (c = this[d]; c && c !== b; c = c.parentNode) if (c.nodeType < 11 && (g ? g.index(c) > -1 : c.nodeType === 1 && jQuery.find.matchesSelector(c, a))) {
                c = f.push(c);
                break
            }
            return this.pushStack(f.length > 1 ? jQuery.unique(f) : f)
        },
        index: function(a) {
            return a ? typeof a == "string" ? core_indexOf.call(jQuery(a), this[0]) : core_indexOf.call(this, a.jquery ? a[0] : a) : this[0] && this[0].parentNode ? this.first().prevAll().length: -1
        },
        add: function(a, b) {
            var c = typeof a == "string" ? jQuery(a, b) : jQuery.makeArray(a && a.nodeType ? [a] : a),
            d = jQuery.merge(this.get(), c);
            return this.pushStack(jQuery.unique(d))
        },
        addBack: function(a) {
            return this.add(a == null ? this.prevObject: this.prevObject.filter(a))
        }
    }),
    jQuery.each({
        parent: function(a) {
            var b = a.parentNode;
            return b && b.nodeType !== 11 ? b: null
        },
        parents: function(a) {
            return jQuery.dir(a, "parentNode")
        },
        parentsUntil: function(a, b, c) {
            return jQuery.dir(a, "parentNode", c)
        },
        next: function(a) {
            return sibling(a, "nextSibling")
        },
        prev: function(a) {
            return sibling(a, "previousSibling")
        },
        nextAll: function(a) {
            return jQuery.dir(a, "nextSibling")
        },
        prevAll: function(a) {
            return jQuery.dir(a, "previousSibling")
        },
        nextUntil: function(a, b, c) {
            return jQuery.dir(a, "nextSibling", c)
        },
        prevUntil: function(a, b, c) {
            return jQuery.dir(a, "previousSibling", c)
        },
        siblings: function(a) {
            return jQuery.sibling((a.parentNode || {}).firstChild, a)
        },
        children: function(a) {
            return jQuery.sibling(a.firstChild)
        },
        contents: function(a) {
            return jQuery.nodeName(a, "iframe") ? a.contentDocument || a.contentWindow.document: jQuery.merge([], a.childNodes)
        }
    },
    function(a, b) {
        jQuery.fn[a] = function(c, d) {
            var e = jQuery.map(this, b, c);
            return a.slice( - 5) !== "Until" && (d = c),
            d && typeof d == "string" && (e = jQuery.filter(d, e)),
            this.length > 1 && (guaranteedUnique[a] || jQuery.unique(e), a[0] === "p" && e.reverse()),
            this.pushStack(e)
        }
    }),
    jQuery.extend({
        filter: function(a, b, c) {
            var d = b[0];
            return c && (a = ":not(" + a + ")"),
            b.length === 1 && d.nodeType === 1 ? jQuery.find.matchesSelector(d, a) ? [d] : [] : jQuery.find.matches(a, jQuery.grep(b,
            function(a) {
                return a.nodeType === 1
            }))
        },
        dir: function(a, b, c) {
            var d = [],
            e = c !== undefined;
            while ((a = a[b]) && a.nodeType !== 9) if (a.nodeType === 1) {
                if (e && jQuery(a).is(c)) break;
                d.push(a)
            }
            return d
        },
        sibling: function(a, b) {
            var c = [];
            for (; a; a = a.nextSibling) a.nodeType === 1 && a !== b && c.push(a);
            return c
        }
    });
    var rxhtmlTag = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,
    rtagName = /<([\w:]+)/,
    rhtml = /<|&#?\w+;/,
    rnoInnerhtml = /<(?:script|style|link)/i,
    manipulation_rcheckableType = /^(?:checkbox|radio)$/i,
    rchecked = /checked\s*(?:[^=]|=\s*.checked.)/i,
    rscriptType = /^$|\/(?:java|ecma)script/i,
    rscriptTypeMasked = /^true\/(.*)/,
    rcleanScript = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g,
    wrapMap = {
        option: [1, "<select multiple='multiple'>", "</select>"],
        thead: [1, "<table>", "</table>"],
        tr: [2, "<table><tbody>", "</tbody></table>"],
        td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
        _default: [0, "", ""]
    };
    wrapMap.optgroup = wrapMap.option,
    wrapMap.tbody = wrapMap.tfoot = wrapMap.colgroup = wrapMap.caption = wrapMap.col = wrapMap.thead,
    wrapMap.th = wrapMap.td,
    jQuery.fn.extend({
        text: function(a) {
            return jQuery.access(this,
            function(a) {
                return a === undefined ? jQuery.text(this) : this.empty().append((this[0] && this[0].ownerDocument || document).createTextNode(a))
            },
            null, a, arguments.length)
        },
        append: function() {
            return this.domManip(arguments,
            function(a) {
                if (this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9) {
                    var b = manipulationTarget(this, a);
                    b.appendChild(a)
                }
            })
        },
        prepend: function() {
            return this.domManip(arguments,
            function(a) {
                if (this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9) {
                    var b = manipulationTarget(this, a);
                    b.insertBefore(a, b.firstChild)
                }
            })
        },
        before: function() {
            return this.domManip(arguments,
            function(a) {
                this.parentNode && this.parentNode.insertBefore(a, this)
            })
        },
        after: function() {
            return this.domManip(arguments,
            function(a) {
                this.parentNode && this.parentNode.insertBefore(a, this.nextSibling)
            })
        },
        remove: function(a, b) {
            var c, d = a ? jQuery.filter(a, this) : this,
            e = 0;
            for (;
            (c = d[e]) != null; e++) ! b && c.nodeType === 1 && jQuery.cleanData(getAll(c)),
            c.parentNode && (b && jQuery.contains(c.ownerDocument, c) && setGlobalEval(getAll(c, "script")), c.parentNode.removeChild(c));
            return this
        },
        empty: function() {
            var a, b = 0;
            for (;
            (a = this[b]) != null; b++) a.nodeType === 1 && (jQuery.cleanData(getAll(a, !1)), a.textContent = "");
            return this
        },
        clone: function(a, b) {
            return a = a == null ? !1 : a,
            b = b == null ? a: b,
            this.map(function() {
                return jQuery.clone(this, a, b)
            })
        },
        html: function(a) {
            return jQuery.access(this,
            function(a) {
                var b = this[0] || {},
                c = 0,
                d = this.length;
                if (a === undefined && b.nodeType === 1) return b.innerHTML;
                if (typeof a == "string" && !rnoInnerhtml.test(a) && !wrapMap[(rtagName.exec(a) || ["", ""])[1].toLowerCase()]) {
                    a = a.replace(rxhtmlTag, "<$1></$2>");
                    try {
                        for (; c < d; c++) b = this[c] || {},
                        b.nodeType === 1 && (jQuery.cleanData(getAll(b, !1)), b.innerHTML = a);
                        b = 0
                    } catch(e) {}
                }
                b && this.empty().append(a)
            },
            null, a, arguments.length)
        },
        replaceWith: function() {
            var a = jQuery.map(this,
            function(a) {
                return [a.nextSibling, a.parentNode]
            }),
            b = 0;
            return this.domManip(arguments,
            function(c) {
                var d = a[b++],
                e = a[b++];
                e && (jQuery(this).remove(), e.insertBefore(c, d))
            },
            !0),
            b ? this: this.remove()
        },
        detach: function(a) {
            return this.remove(a, !0)
        },
        domManip: function(a, b, c) {
            a = core_concat.apply([], a);
            var d, e, f, g, h, i, j = 0,
            k = this.length,
            l = this,
            m = k - 1,
            n = a[0],
            o = jQuery.isFunction(n);
            if (o || !(k <= 1 || typeof n != "string" || jQuery.support.checkClone || !rchecked.test(n))) return this.each(function(d) {
                var e = l.eq(d);
                o && (a[0] = n.call(this, d, e.html())),
                e.domManip(a, b, c)
            });
            if (k) {
                d = jQuery.buildFragment(a, this[0].ownerDocument, !1, !c && this),
                e = d.firstChild,
                d.childNodes.length === 1 && (d = e);
                if (e) {
                    f = jQuery.map(getAll(d, "script"), disableScript),
                    g = f.length;
                    for (; j < k; j++) h = d,
                    j !== m && (h = jQuery.clone(h, !0, !0), g && jQuery.merge(f, getAll(h, "script"))),
                    b.call(this[j], h, j);
                    if (g) {
                        i = f[f.length - 1].ownerDocument,
                        jQuery.map(f, restoreScript);
                        for (j = 0; j < g; j++) h = f[j],
                        rscriptType.test(h.type || "") && !data_priv.access(h, "globalEval") && jQuery.contains(i, h) && (h.src ? jQuery._evalUrl(h.src) : jQuery.globalEval(h.textContent.replace(rcleanScript, "")))
                    }
                }
            }
            return this
        }
    }),
    jQuery.each({
        appendTo: "append",
        prependTo: "prepend",
        insertBefore: "before",
        insertAfter: "after",
        replaceAll: "replaceWith"
    },
    function(a, b) {
        jQuery.fn[a] = function(a) {
            var c, d = [],
            e = jQuery(a),
            f = e.length - 1,
            g = 0;
            for (; g <= f; g++) c = g === f ? this: this.clone(!0),
            jQuery(e[g])[b](c),
            core_push.apply(d, c.get());
            return this.pushStack(d)
        }
    }),
    jQuery.extend({
        clone: function(a, b, c) {
            var d, e, f, g, h = a.cloneNode(!0),
            i = jQuery.contains(a.ownerDocument, a);
            if (!jQuery.support.noCloneChecked && (a.nodeType === 1 || a.nodeType === 11) && !jQuery.isXMLDoc(a)) {
                g = getAll(h),
                f = getAll(a);
                for (d = 0, e = f.length; d < e; d++) fixInput(f[d], g[d])
            }
            if (b) if (c) {
                f = f || getAll(a),
                g = g || getAll(h);
                for (d = 0, e = f.length; d < e; d++) cloneCopyEvent(f[d], g[d])
            } else cloneCopyEvent(a, h);
            return g = getAll(h, "script"),
            g.length > 0 && setGlobalEval(g, !i && getAll(a, "script")),
            h
        },
        buildFragment: function(a, b, c, d) {
            var e, f, g, h, i, j, k = 0,
            l = a.length,
            m = b.createDocumentFragment(),
            n = [];
            for (; k < l; k++) {
                e = a[k];
                if (e || e === 0) if (jQuery.type(e) === "object") jQuery.merge(n, e.nodeType ? [e] : e);
                else if (!rhtml.test(e)) n.push(b.createTextNode(e));
                else {
                    f = f || m.appendChild(b.createElement("div")),
                    g = (rtagName.exec(e) || ["", ""])[1].toLowerCase(),
                    h = wrapMap[g] || wrapMap._default,
                    f.innerHTML = h[1] + e.replace(rxhtmlTag, "<$1></$2>") + h[2],
                    j = h[0];
                    while (j--) f = f.firstChild;
                    jQuery.merge(n, f.childNodes),
                    f = m.firstChild,
                    f.textContent = ""
                }
            }
            m.textContent = "",
            k = 0;
            while (e = n[k++]) {
                if (d && jQuery.inArray(e, d) !== -1) continue;
                i = jQuery.contains(e.ownerDocument, e),
                f = getAll(m.appendChild(e), "script"),
                i && setGlobalEval(f);
                if (c) {
                    j = 0;
                    while (e = f[j++]) rscriptType.test(e.type || "") && c.push(e)
                }
            }
            return m
        },
        cleanData: function(a) {
            var b, c, d, e = a.length,
            f = 0,
            g = jQuery.event.special;
            for (; f < e; f++) {
                c = a[f];
                if (jQuery.acceptData(c)) {
                    b = data_priv.access(c);
                    if (b) for (d in b.events) g[d] ? jQuery.event.remove(c, d) : jQuery.removeEvent(c, d, b.handle)
                }
                data_user.discard(c),
                data_priv.discard(c)
            }
        },
        _evalUrl: function(a) {
            return jQuery.ajax({
                url: a,
                type: "GET",
                dataType: "text",
                async: !1,
                global: !1,
                success: jQuery.globalEval
            })
        }
    }),
    jQuery.fn.extend({
        wrapAll: function(a) {
            var b;
            return jQuery.isFunction(a) ? this.each(function(b) {
                jQuery(this).wrapAll(a.call(this, b))
            }) : (this[0] && (b = jQuery(a, this[0].ownerDocument).eq(0).clone(!0), this[0].parentNode && b.insertBefore(this[0]), b.map(function() {
                var a = this;
                while (a.firstElementChild) a = a.firstElementChild;
                return a
            }).append(this)), this)
        },
        wrapInner: function(a) {
            return jQuery.isFunction(a) ? this.each(function(b) {
                jQuery(this).wrapInner(a.call(this, b))
            }) : this.each(function() {
                var b = jQuery(this),
                c = b.contents();
                c.length ? c.wrapAll(a) : b.append(a)
            })
        },
        wrap: function(a) {
            var b = jQuery.isFunction(a);
            return this.each(function(c) {
                jQuery(this).wrapAll(b ? a.call(this, c) : a)
            })
        },
        unwrap: function() {
            return this.parent().each(function() {
                jQuery.nodeName(this, "body") || jQuery(this).replaceWith(this.childNodes)
            }).end()
        }
    });
    var curCSS, iframe, rdisplayswap = /^(none|table(?!-c[ea]).+)/,
    rmargin = /^margin/,
    rnumsplit = new RegExp("^(" + core_pnum + ")(.*)$", "i"),
    rnumnonpx = new RegExp("^(" + core_pnum + ")(?!px)[a-z%]+$", "i"),
    rrelNum = new RegExp("^([+-])=(" + core_pnum + ")", "i"),
    elemdisplay = {
        BODY: "block"
    },
    cssShow = {
        position: "absolute",
        visibility: "hidden",
        display: "block"
    },
    cssNormalTransform = {
        letterSpacing: 0,
        fontWeight: 400
    },
    cssExpand = ["Top", "Right", "Bottom", "Left"],
    cssPrefixes = ["Webkit", "O", "Moz", "ms"];
    jQuery.fn.extend({
        css: function(a, b) {
            return jQuery.access(this,
            function(a, b, c) {
                var d, e, f = {},
                g = 0;
                if (jQuery.isArray(b)) {
                    d = getStyles(a),
                    e = b.length;
                    for (; g < e; g++) f[b[g]] = jQuery.css(a, b[g], !1, d);
                    return f
                }
                return c !== undefined ? jQuery.style(a, b, c) : jQuery.css(a, b)
            },
            a, b, arguments.length > 1)
        },
        show: function() {
            return showHide(this, !0)
        },
        hide: function() {
            return showHide(this)
        },
        toggle: function(a) {
            var b = typeof a == "boolean";
            return this.each(function() { (b ? a: isHidden(this)) ? jQuery(this).show() : jQuery(this).hide()
            })
        }
    }),
    jQuery.extend({
        cssHooks: {
            opacity: {
                get: function(a, b) {
                    if (b) {
                        var c = curCSS(a, "opacity");
                        return c === "" ? "1": c
                    }
                }
            }
        },
        cssNumber: {
            columnCount: !0,
            fillOpacity: !0,
            fontWeight: !0,
            lineHeight: !0,
            opacity: !0,
            orphans: !0,
            widows: !0,
            zIndex: !0,
            zoom: !0
        },
        cssProps: {
            "float": "cssFloat"
        },
        style: function(a, b, c, d) {
            if (!a || a.nodeType === 3 || a.nodeType === 8 || !a.style) return;
            var e, f, g, h = jQuery.camelCase(b),
            i = a.style;
            b = jQuery.cssProps[h] || (jQuery.cssProps[h] = vendorPropName(i, h)),
            g = jQuery.cssHooks[b] || jQuery.cssHooks[h];
            if (c === undefined) return g && "get" in g && (e = g.get(a, !1, d)) !== undefined ? e: i[b];
            f = typeof c,
            f === "string" && (e = rrelNum.exec(c)) && (c = (e[1] + 1) * e[2] + parseFloat(jQuery.css(a, b)), f = "number");
            if (c == null || f === "number" && isNaN(c)) return;
            f === "number" && !jQuery.cssNumber[h] && (c += "px"),
            !jQuery.support.clearCloneStyle && c === "" && b.indexOf("background") === 0 && (i[b] = "inherit");
            if (!g || !("set" in g) || (c = g.set(a, c, d)) !== undefined) i[b] = c
        },
        css: function(a, b, c, d) {
            var e, f, g, h = jQuery.camelCase(b);
            return b = jQuery.cssProps[h] || (jQuery.cssProps[h] = vendorPropName(a.style, h)),
            g = jQuery.cssHooks[b] || jQuery.cssHooks[h],
            g && "get" in g && (e = g.get(a, !0, c)),
            e === undefined && (e = curCSS(a, b, d)),
            e === "normal" && b in cssNormalTransform && (e = cssNormalTransform[b]),
            c === "" || c ? (f = parseFloat(e), c === !0 || jQuery.isNumeric(f) ? f || 0 : e) : e
        }
    }),
    curCSS = function(a, b, c) {
        var d, e, f, g = c || getStyles(a),
        h = g ? g.getPropertyValue(b) || g[b] : undefined,
        i = a.style;
        return g && (h === "" && !jQuery.contains(a.ownerDocument, a) && (h = jQuery.style(a, b)), rnumnonpx.test(h) && rmargin.test(b) && (d = i.width, e = i.minWidth, f = i.maxWidth, i.minWidth = i.maxWidth = i.width = h, h = g.width, i.width = d, i.minWidth = e, i.maxWidth = f)),
        h
    },
    jQuery.each(["height", "width"],
    function(a, b) {
        jQuery.cssHooks[b] = {
            get: function(a, c, d) {
                if (c) return a.offsetWidth === 0 && rdisplayswap.test(jQuery.css(a, "display")) ? jQuery.swap(a, cssShow,
                function() {
                    return getWidthOrHeight(a, b, d)
                }) : getWidthOrHeight(a, b, d)
            },
            set: function(a, c, d) {
                var e = d && getStyles(a);
                return setPositiveNumber(a, c, d ? augmentWidthOrHeight(a, b, d, jQuery.support.boxSizing && jQuery.css(a, "boxSizing", !1, e) === "border-box", e) : 0)
            }
        }
    }),
    jQuery(function() {
        jQuery.support.reliableMarginRight || (jQuery.cssHooks.marginRight = {
            get: function(a, b) {
                if (b) return jQuery.swap(a, {
                    display: "inline-block"
                },
                curCSS, [a, "marginRight"])
            }
        }),
        !jQuery.support.pixelPosition && jQuery.fn.position && jQuery.each(["top", "left"],
        function(a, b) {
            jQuery.cssHooks[b] = {
                get: function(a, c) {
                    if (c) return c = curCSS(a, b),
                    rnumnonpx.test(c) ? jQuery(a).position()[b] + "px": c
                }
            }
        })
    }),
    jQuery.expr && jQuery.expr.filters && (jQuery.expr.filters.hidden = function(a) {
        return a.offsetWidth <= 0 && a.offsetHeight <= 0
    },
    jQuery.expr.filters.visible = function(a) {
        return ! jQuery.expr.filters.hidden(a)
    }),
    jQuery.each({
        margin: "",
        padding: "",
        border: "Width"
    },
    function(a, b) {
        jQuery.cssHooks[a + b] = {
            expand: function(c) {
                var d = 0,
                e = {},
                f = typeof c == "string" ? c.split(" ") : [c];
                for (; d < 4; d++) e[a + cssExpand[d] + b] = f[d] || f[d - 2] || f[0];
                return e
            }
        },
        rmargin.test(a) || (jQuery.cssHooks[a + b].set = setPositiveNumber)
    });
    var r20 = /%20/g,
    rbracket = /\[\]$/,
    rCRLF = /\r?\n/g,
    rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
    rsubmittable = /^(?:input|select|textarea|keygen)/i;
    jQuery.fn.extend({
        serialize: function() {
            return jQuery.param(this.serializeArray())
        },
        serializeArray: function() {
            return this.map(function() {
                var a = jQuery.prop(this, "elements");
                return a ? jQuery.makeArray(a) : this
            }).filter(function() {
                var a = this.type;
                return this.name && !jQuery(this).is(":disabled") && rsubmittable.test(this.nodeName) && !rsubmitterTypes.test(a) && (this.checked || !manipulation_rcheckableType.test(a))
            }).map(function(a, b) {
                var c = jQuery(this).val();
                return c == null ? null: jQuery.isArray(c) ? jQuery.map(c,
                function(a) {
                    return {
                        name: b.name,
                        value: a.replace(rCRLF, "\r\n")
                    }
                }) : {
                    name: b.name,
                    value: c.replace(rCRLF, "\r\n")
                }
            }).get()
        }
    }),
    jQuery.param = function(a, b) {
        var c, d = [],
        e = function(a, b) {
            b = jQuery.isFunction(b) ? b() : b == null ? "": b,
            d[d.length] = encodeURIComponent(a) + "=" + encodeURIComponent(b)
        };
        b === undefined && (b = jQuery.ajaxSettings && jQuery.ajaxSettings.traditional);
        if (jQuery.isArray(a) || a.jquery && !jQuery.isPlainObject(a)) jQuery.each(a,
        function() {
            e(this.name, this.value)
        });
        else for (c in a) buildParams(c, a[c], b, e);
        return d.join("&").replace(r20, "+")
    },
    jQuery.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "),
    function(a, b) {
        jQuery.fn[b] = function(a, c) {
            return arguments.length > 0 ? this.on(b, null, a, c) : this.trigger(b)
        }
    }),
    jQuery.fn.extend({
        hover: function(a, b) {
            return this.mouseenter(a).mouseleave(b || a)
        },
        bind: function(a, b, c) {
            return this.on(a, null, b, c)
        },
        unbind: function(a, b) {
            return this.off(a, null, b)
        },
        delegate: function(a, b, c, d) {
            return this.on(b, a, c, d)
        },
        undelegate: function(a, b, c) {
            return arguments.length === 1 ? this.off(a, "**") : this.off(b, a || "**", c)
        }
    });
    var ajaxLocParts, ajaxLocation, ajax_nonce = jQuery.now(),
    ajax_rquery = /\?/,
    rhash = /#.*$/,
    rts = /([?&])_=[^&]*/,
    rheaders = /^(.*?):[ \t]*([^\r\n]*)$/mg,
    rlocalProtocol = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
    rnoContent = /^(?:GET|HEAD)$/,
    rprotocol = /^\/\//,
    rurl = /^([\w.+-]+:)(?:\/\/([^\/?#:]*)(?::(\d+)|)|)/,
    _load = jQuery.fn.load,
    prefilters = {},
    transports = {},
    allTypes = "*/".concat("*");
    try {
        ajaxLocation = location.href
    } catch(e) {
        ajaxLocation = document.createElement("a"),
        ajaxLocation.href = "",
        ajaxLocation = ajaxLocation.href
    }
    ajaxLocParts = rurl.exec(ajaxLocation.toLowerCase()) || [],
    jQuery.fn.load = function(a, b, c) {
        if (typeof a != "string" && _load) return _load.apply(this, arguments);
        var d, e, f, g = this,
        h = a.indexOf(" ");
        return h >= 0 && (d = a.slice(h), a = a.slice(0, h)),
        jQuery.isFunction(b) ? (c = b, b = undefined) : b && typeof b == "object" && (e = "POST"),
        g.length > 0 && jQuery.ajax({
            url: a,
            type: e,
            dataType: "html",
            data: b
        }).done(function(a) {
            f = arguments,
            g.html(d ? jQuery("<div>").append(jQuery.parseHTML(a)).find(d) : a)
        }).complete(c &&
        function(a, b) {
            g.each(c, f || [a.responseText, b, a])
        }),
        this
    },
    jQuery.each(["ajaxStart", "ajaxStop", "ajaxComplete", "ajaxError", "ajaxSuccess", "ajaxSend"],
    function(a, b) {
        jQuery.fn[b] = function(a) {
            return this.on(b, a)
        }
    }),
    jQuery.extend({
        active: 0,
        lastModified: {},
        etag: {},
        ajaxSettings: {
            url: ajaxLocation,
            type: "GET",
            isLocal: rlocalProtocol.test(ajaxLocParts[1]),
            global: !0,
            processData: !0,
            async: !0,
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            accepts: {
                "*": allTypes,
                text: "text/plain",
                html: "text/html",
                xml: "application/xml, text/xml",
                json: "application/json, text/javascript"
            },
            contents: {
                xml: /xml/,
                html: /html/,
                json: /json/
            },
            responseFields: {
                xml: "responseXML",
                text: "responseText",
                json: "responseJSON"
            },
            converters: {
                "* text": String,
                "text html": !0,
                "text json": jQuery.parseJSON,
                "text xml": jQuery.parseXML
            },
            flatOptions: {
                url: !0,
                context: !0
            }
        },
        ajaxSetup: function(a, b) {
            return b ? ajaxExtend(ajaxExtend(a, jQuery.ajaxSettings), b) : ajaxExtend(jQuery.ajaxSettings, a)
        },
        ajaxPrefilter: addToPrefiltersOrTransports(prefilters),
        ajaxTransport: addToPrefiltersOrTransports(transports),
        ajax: function(a, b) {
            function w(a, b, f, h) {
                var j, q, r, t, v, w = b;
                if (s === 2) return;
                s = 2,
                g && clearTimeout(g),
                c = undefined,
                e = h || "",
                u.readyState = a > 0 ? 4 : 0,
                j = a >= 200 && a < 300 || a === 304,
                f && (t = ajaxHandleResponses(k, u, f)),
                t = ajaxConvert(k, t, u, j);
                if (j) k.ifModified && (v = u.getResponseHeader("Last-Modified"), v && (jQuery.lastModified[d] = v), v = u.getResponseHeader("etag"), v && (jQuery.etag[d] = v)),
                a === 204 ? w = "nocontent": a === 304 ? w = "notmodified": (w = t.state, q = t.data, r = t.error, j = !r);
                else {
                    r = w;
                    if (a || !w) w = "error",
                    a < 0 && (a = 0)
                }
                u.status = a,
                u.statusText = (b || w) + "",
                j ? n.resolveWith(l, [q, w, u]) : n.rejectWith(l, [u, w, r]),
                u.statusCode(p),
                p = undefined,
                i && m.trigger(j ? "ajaxSuccess": "ajaxError", [u, k, j ? q: r]),
                o.fireWith(l, [u, w]),
                i && (m.trigger("ajaxComplete", [u, k]), --jQuery.active || jQuery.event.trigger("ajaxStop"))
            }
            typeof a == "object" && (b = a, a = undefined),
            b = b || {};
            var c, d, e, f, g, h, i, j, k = jQuery.ajaxSetup({},
            b),
            l = k.context || k,
            m = k.context && (l.nodeType || l.jquery) ? jQuery(l) : jQuery.event,
            n = jQuery.Deferred(),
            o = jQuery.Callbacks("once memory"),
            p = k.statusCode || {},
            q = {},
            r = {},
            s = 0,
            t = "canceled",
            u = {
                readyState: 0,
                getResponseHeader: function(a) {
                    var b;
                    if (s === 2) {
                        if (!f) {
                            f = {};
                            while (b = rheaders.exec(e)) f[b[1].toLowerCase()] = b[2]
                        }
                        b = f[a.toLowerCase()]
                    }
                    return b == null ? null: b
                },
                getAllResponseHeaders: function() {
                    return s === 2 ? e: null
                },
                setRequestHeader: function(a, b) {
                    var c = a.toLowerCase();
                    return s || (a = r[c] = r[c] || a, q[a] = b),
                    this
                },
                overrideMimeType: function(a) {
                    return s || (k.mimeType = a),
                    this
                },
                statusCode: function(a) {
                    var b;
                    if (a) if (s < 2) for (b in a) p[b] = [p[b], a[b]];
                    else u.always(a[u.status]);
                    return this
                },
                abort: function(a) {
                    var b = a || t;
                    return c && c.abort(b),
                    w(0, b),
                    this
                }
            };
            n.promise(u).complete = o.add,
            u.success = u.done,
            u.error = u.fail,
            k.url = ((a || k.url || ajaxLocation) + "").replace(rhash, "").replace(rprotocol, ajaxLocParts[1] + "//"),
            k.type = b.method || b.type || k.method || k.type,
            k.dataTypes = jQuery.trim(k.dataType || "*").toLowerCase().match(core_rnotwhite) || [""],
            k.crossDomain == null && (h = rurl.exec(k.url.toLowerCase()), k.crossDomain = !(!h || h[1] === ajaxLocParts[1] && h[2] === ajaxLocParts[2] && (h[3] || (h[1] === "http:" ? "80": "443")) === (ajaxLocParts[3] || (ajaxLocParts[1] === "http:" ? "80": "443")))),
            k.data && k.processData && typeof k.data != "string" && (k.data = jQuery.param(k.data, k.traditional)),
            inspectPrefiltersOrTransports(prefilters, k, b, u);
            if (s === 2) return u;
            i = k.global,
            i && jQuery.active++===0 && jQuery.event.trigger("ajaxStart"),
            k.type = k.type.toUpperCase(),
            k.hasContent = !rnoContent.test(k.type),
            d = k.url,
            k.hasContent || (k.data && (d = k.url += (ajax_rquery.test(d) ? "&": "?") + k.data, delete k.data), k.cache === !1 && (k.url = rts.test(d) ? d.replace(rts, "$1_=" + ajax_nonce++) : d + (ajax_rquery.test(d) ? "&": "?") + "_=" + ajax_nonce++)),
            k.ifModified && (jQuery.lastModified[d] && u.setRequestHeader("If-Modified-Since", jQuery.lastModified[d]), jQuery.etag[d] && u.setRequestHeader("If-None-Match", jQuery.etag[d])),
            (k.data && k.hasContent && k.contentType !== !1 || b.contentType) && u.setRequestHeader("Content-Type", k.contentType),
            u.setRequestHeader("Accept", k.dataTypes[0] && k.accepts[k.dataTypes[0]] ? k.accepts[k.dataTypes[0]] + (k.dataTypes[0] !== "*" ? ", " + allTypes + "; q=0.01": "") : k.accepts["*"]);
            for (j in k.headers) u.setRequestHeader(j, k.headers[j]);
            if (!k.beforeSend || k.beforeSend.call(l, u, k) !== !1 && s !== 2) {
                t = "abort";
                for (j in {
                    success: 1,
                    error: 1,
                    complete: 1
                }) u[j](k[j]);
                c = inspectPrefiltersOrTransports(transports, k, b, u);
                if (!c) w( - 1, "No Transport");
                else {
                    u.readyState = 1,
                    i && m.trigger("ajaxSend", [u, k]),
                    k.async && k.timeout > 0 && (g = setTimeout(function() {
                        u.abort("timeout")
                    },
                    k.timeout));
                    try {
                        s = 1,
                        c.send(q, w)
                    } catch(v) {
                        if (s < 2) w( - 1, v);
                        else throw v
                    }
                }
                return u
            }
            return u.abort()
        },
        getJSON: function(a, b, c) {
            return jQuery.get(a, b, c, "json")
        },
        getScript: function(a, b) {
            return jQuery.get(a, undefined, b, "script")
        }
    }),
    jQuery.each(["get", "post"],
    function(a, b) {
        jQuery[b] = function(a, c, d, e) {
            return jQuery.isFunction(c) && (e = e || d, d = c, c = undefined),
            jQuery.ajax({
                url: a,
                type: b,
                dataType: e,
                data: c,
                success: d
            })
        }
    }),
    jQuery.ajaxSetup({
        accepts: {
            script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"
        },
        contents: {
            script: /(?:java|ecma)script/
        },
        converters: {
            "text script": function(a) {
                return jQuery.globalEval(a),
                a
            }
        }
    }),
    jQuery.ajaxPrefilter("script",
    function(a) {
        a.cache === undefined && (a.cache = !1),
        a.crossDomain && (a.type = "GET")
    }),
    jQuery.ajaxTransport("script",
    function(a) {
        if (a.crossDomain) {
            var b, c;
            return {
                send: function(d, e) {
                    b = jQuery("<script>").prop({
                        async: !0,
                        charset: a.scriptCharset,
                        src: a.url
                    }).on("load error", c = function(a) {
                        b.remove(),
                        c = null,
                        a && e(a.type === "error" ? 404 : 200, a.type)
                    }),
                    document.head.appendChild(b[0])
                },
                abort: function() {
                    c && c()
                }
            }
        }
    });
    var oldCallbacks = [],
    rjsonp = /(=)\?(?=&|$)|\?\?/;
    jQuery.ajaxSetup({
        jsonp: "callback",
        jsonpCallback: function() {
            var a = oldCallbacks.pop() || jQuery.expando + "_" + ajax_nonce++;
            return this[a] = !0,
            a
        }
    }),
    jQuery.ajaxPrefilter("json jsonp",
    function(a, b, c) {
        var d, e, f, g = a.jsonp !== !1 && (rjsonp.test(a.url) ? "url": typeof a.data == "string" && !(a.contentType || "").indexOf("application/x-www-form-urlencoded") && rjsonp.test(a.data) && "data");
        if (g || a.dataTypes[0] === "jsonp") return d = a.jsonpCallback = jQuery.isFunction(a.jsonpCallback) ? a.jsonpCallback() : a.jsonpCallback,
        g ? a[g] = a[g].replace(rjsonp, "$1" + d) : a.jsonp !== !1 && (a.url += (ajax_rquery.test(a.url) ? "&": "?") + a.jsonp + "=" + d),
        a.converters["script json"] = function() {
            return f || jQuery.error(d + " was not called"),
            f[0]
        },
        a.dataTypes[0] = "json",
        e = window[d],
        window[d] = function() {
            f = arguments
        },
        c.always(function() {
            window[d] = e,
            a[d] && (a.jsonpCallback = b.jsonpCallback, oldCallbacks.push(d)),
            f && jQuery.isFunction(e) && e(f[0]),
            f = e = undefined
        }),
        "script"
    }),
    jQuery.ajaxSettings.xhr = function() {
        try {
            return new XMLHttpRequest
        } catch(a) {}
    };
    var xhrSupported = jQuery.ajaxSettings.xhr(),
    xhrSuccessStatus = {
        0 : 200,
        1223 : 204
    },
    xhrId = 0,
    xhrCallbacks = {};
    window.ActiveXObject && jQuery(window).on("unload",
    function() {
        for (var a in xhrCallbacks) xhrCallbacks[a]();
        xhrCallbacks = undefined
    }),
    jQuery.support.cors = !!xhrSupported && "withCredentials" in xhrSupported,
    jQuery.support.ajax = xhrSupported = !!xhrSupported,
    jQuery.ajaxTransport(function(a) {
        var b;
        if (jQuery.support.cors || xhrSupported && !a.crossDomain) return {
            send: function(c, d) {
                var e, f, g = a.xhr();
                g.open(a.type, a.url, a.async, a.username, a.password);
                if (a.xhrFields) for (e in a.xhrFields) g[e] = a.xhrFields[e];
                a.mimeType && g.overrideMimeType && g.overrideMimeType(a.mimeType),
                !a.crossDomain && !c["X-Requested-With"] && (c["X-Requested-With"] = "XMLHttpRequest");
                for (e in c) g.setRequestHeader(e, c[e]);
                b = function(a) {
                    return function() {
                        b && (delete xhrCallbacks[f], b = g.onload = g.onerror = null, a === "abort" ? g.abort() : a === "error" ? d(g.status || 404, g.statusText) : d(xhrSuccessStatus[g.status] || g.status, g.statusText, typeof g.responseText == "string" ? {
                            text: g.responseText
                        }: undefined, g.getAllResponseHeaders()))
                    }
                },
                g.onload = b(),
                g.onerror = b("error"),
                b = xhrCallbacks[f = xhrId++] = b("abort"),
                g.send(a.hasContent && a.data || null)
            },
            abort: function() {
                b && b()
            }
        }
    });
    var fxNow, timerId, rfxtypes = /^(?:toggle|show|hide)$/,
    rfxnum = new RegExp("^(?:([+-])=|)(" + core_pnum + ")([a-z%]*)$", "i"),
    rrun = /queueHooks$/,
    animationPrefilters = [defaultPrefilter],
    tweeners = {
        "*": [function(a, b) {
            var c, d, e = this.createTween(a, b),
            f = rfxnum.exec(b),
            g = e.cur(),
            h = +g || 0,
            i = 1,
            j = 20;
            if (f) {
                c = +f[2],
                d = f[3] || (jQuery.cssNumber[a] ? "": "px");
                if (d !== "px" && h) {
                    h = jQuery.css(e.elem, a, !0) || c || 1;
                    do i = i || ".5",
                    h /= i,
                    jQuery.style(e.elem, a, h + d);
                    while (i !== (i = e.cur() / g) && i !== 1 && --j)
                }
                e.unit = d,
                e.start = h,
                e.end = f[1] ? h + (f[1] + 1) * c: c
            }
            return e
        }]
    };
    jQuery.Animation = jQuery.extend(Animation, {
        tweener: function(a, b) {
            jQuery.isFunction(a) ? (b = a, a = ["*"]) : a = a.split(" ");
            var c, d = 0,
            e = a.length;
            for (; d < e; d++) c = a[d],
            tweeners[c] = tweeners[c] || [],
            tweeners[c].unshift(b)
        },
        prefilter: function(a, b) {
            b ? animationPrefilters.unshift(a) : animationPrefilters.push(a)
        }
    }),
    jQuery.Tween = Tween,
    Tween.prototype = {
        constructor: Tween,
        init: function(a, b, c, d, e, f) {
            this.elem = a,
            this.prop = c,
            this.easing = e || "swing",
            this.options = b,
            this.start = this.now = this.cur(),
            this.end = d,
            this.unit = f || (jQuery.cssNumber[c] ? "": "px")
        },
        cur: function() {
            var a = Tween.propHooks[this.prop];
            return a && a.get ? a.get(this) : Tween.propHooks._default.get(this)
        },
        run: function(a) {
            var b, c = Tween.propHooks[this.prop];
            return this.options.duration ? this.pos = b = jQuery.easing[this.easing](a, this.options.duration * a, 0, 1, this.options.duration) : this.pos = b = a,
            this.now = (this.end - this.start) * b + this.start,
            this.options.step && this.options.step.call(this.elem, this.now, this),
            c && c.set ? c.set(this) : Tween.propHooks._default.set(this),
            this
        }
    },
    Tween.prototype.init.prototype = Tween.prototype,
    Tween.propHooks = {
        _default: {
            get: function(a) {
                var b;
                return a.elem[a.prop] == null || !!a.elem.style && a.elem.style[a.prop] != null ? (b = jQuery.css(a.elem, a.prop, ""), !b || b === "auto" ? 0 : b) : a.elem[a.prop]
            },
            set: function(a) {
                jQuery.fx.step[a.prop] ? jQuery.fx.step[a.prop](a) : a.elem.style && (a.elem.style[jQuery.cssProps[a.prop]] != null || jQuery.cssHooks[a.prop]) ? jQuery.style(a.elem, a.prop, a.now + a.unit) : a.elem[a.prop] = a.now
            }
        }
    },
    Tween.propHooks.scrollTop = Tween.propHooks.scrollLeft = {
        set: function(a) {
            a.elem.nodeType && a.elem.parentNode && (a.elem[a.prop] = a.now)
        }
    },
    jQuery.each(["toggle", "show", "hide"],
    function(a, b) {
        var c = jQuery.fn[b];
        jQuery.fn[b] = function(a, d, e) {
            return a == null || typeof a == "boolean" ? c.apply(this, arguments) : this.animate(genFx(b, !0), a, d, e)
        }
    }),
    jQuery.fn.extend({
        fadeTo: function(a, b, c, d) {
            return this.filter(isHidden).css("opacity", 0).show().end().animate({
                opacity: b
            },
            a, c, d)
        },
        animate: function(a, b, c, d) {
            var e = jQuery.isEmptyObject(a),
            f = jQuery.speed(b, c, d),
            g = function() {
                var b = Animation(this, jQuery.extend({},
                a), f);
                g.finish = function() {
                    b.stop(!0)
                },
                (e || data_priv.get(this, "finish")) && b.stop(!0)
            };
            return g.finish = g,
            e || f.queue === !1 ? this.each(g) : this.queue(f.queue, g)
        },
        stop: function(a, b, c) {
            var d = function(a) {
                var b = a.stop;
                delete a.stop,
                b(c)
            };
            return typeof a != "string" && (c = b, b = a, a = undefined),
            b && a !== !1 && this.queue(a || "fx", []),
            this.each(function() {
                var b = !0,
                e = a != null && a + "queueHooks",
                f = jQuery.timers,
                g = data_priv.get(this);
                if (e) g[e] && g[e].stop && d(g[e]);
                else for (e in g) g[e] && g[e].stop && rrun.test(e) && d(g[e]);
                for (e = f.length; e--;) f[e].elem === this && (a == null || f[e].queue === a) && (f[e].anim.stop(c), b = !1, f.splice(e, 1));
                (b || !c) && jQuery.dequeue(this, a)
            })
        },
        finish: function(a) {
            return a !== !1 && (a = a || "fx"),
            this.each(function() {
                var b, c = data_priv.get(this),
                d = c[a + "queue"],
                e = c[a + "queueHooks"],
                f = jQuery.timers,
                g = d ? d.length: 0;
                c.finish = !0,
                jQuery.queue(this, a, []),
                e && e.cur && e.cur.finish && e.cur.finish.call(this);
                for (b = f.length; b--;) f[b].elem === this && f[b].queue === a && (f[b].anim.stop(!0), f.splice(b, 1));
                for (b = 0; b < g; b++) d[b] && d[b].finish && d[b].finish.call(this);
                delete c.finish
            })
        }
    }),
    jQuery.each({
        slideDown: genFx("show"),
        slideUp: genFx("hide"),
        slideToggle: genFx("toggle"),
        fadeIn: {
            opacity: "show"
        },
        fadeOut: {
            opacity: "hide"
        },
        fadeToggle: {
            opacity: "toggle"
        }
    },
    function(a, b) {
        jQuery.fn[a] = function(a, c, d) {
            return this.animate(b, a, c, d)
        }
    }),
    jQuery.speed = function(a, b, c) {
        var d = a && typeof a == "object" ? jQuery.extend({},
        a) : {
            complete: c || !c && b || jQuery.isFunction(a) && a,
            duration: a,
            easing: c && b || b && !jQuery.isFunction(b) && b
        };
        d.duration = jQuery.fx.off ? 0 : typeof d.duration == "number" ? d.duration: d.duration in jQuery.fx.speeds ? jQuery.fx.speeds[d.duration] : jQuery.fx.speeds._default;
        if (d.queue == null || d.queue === !0) d.queue = "fx";
        return d.old = d.complete,
        d.complete = function() {
            jQuery.isFunction(d.old) && d.old.call(this),
            d.queue && jQuery.dequeue(this, d.queue)
        },
        d
    },
    jQuery.easing = {
        linear: function(a) {
            return a
        },
        swing: function(a) {
            return.5 - Math.cos(a * Math.PI) / 2
        }
    },
    jQuery.timers = [],
    jQuery.fx = Tween.prototype.init,
    jQuery.fx.tick = function() {
        var a, b = jQuery.timers,
        c = 0;
        fxNow = jQuery.now();
        for (; c < b.length; c++) a = b[c],
        !a() && b[c] === a && b.splice(c--, 1);
        b.length || jQuery.fx.stop(),
        fxNow = undefined
    },
    jQuery.fx.timer = function(a) {
        a() && jQuery.timers.push(a) && jQuery.fx.start()
    },
    jQuery.fx.interval = 13,
    jQuery.fx.start = function() {
        timerId || (timerId = setInterval(jQuery.fx.tick, jQuery.fx.interval))
    },
    jQuery.fx.stop = function() {
        clearInterval(timerId),
        timerId = null
    },
    jQuery.fx.speeds = {
        slow: 600,
        fast: 200,
        _default: 400
    },
    jQuery.fx.step = {},
    jQuery.expr && jQuery.expr.filters && (jQuery.expr.filters.animated = function(a) {
        return jQuery.grep(jQuery.timers,
        function(b) {
            return a === b.elem
        }).length
    }),
    jQuery.fn.offset = function(a) {
        if (arguments.length) return a === undefined ? this: this.each(function(b) {
            jQuery.offset.setOffset(this, a, b)
        });
        var b, c, d = this[0],
        e = {
            top: 0,
            left: 0
        },
        f = d && d.ownerDocument;
        if (!f) return;
        return b = f.documentElement,
        jQuery.contains(b, d) ? (typeof d.getBoundingClientRect !== core_strundefined && (e = d.getBoundingClientRect()), c = getWindow(f), {
            top: e.top + c.pageYOffset - b.clientTop,
            left: e.left + c.pageXOffset - b.clientLeft
        }) : e
    },
    jQuery.offset = {
        setOffset: function(a, b, c) {
            var d, e, f, g, h, i, j, k = jQuery.css(a, "position"),
            l = jQuery(a),
            m = {};
            k === "static" && (a.style.position = "relative"),
            h = l.offset(),
            f = jQuery.css(a, "top"),
            i = jQuery.css(a, "left"),
            j = (k === "absolute" || k === "fixed") && (f + i).indexOf("auto") > -1,
            j ? (d = l.position(), g = d.top, e = d.left) : (g = parseFloat(f) || 0, e = parseFloat(i) || 0),
            jQuery.isFunction(b) && (b = b.call(a, c, h)),
            b.top != null && (m.top = b.top - h.top + g),
            b.left != null && (m.left = b.left - h.left + e),
            "using" in b ? b.using.call(a, m) : l.css(m)
        }
    },
    jQuery.fn.extend({
        position: function() {
            if (!this[0]) return;
            var a, b, c = this[0],
            d = {
                top: 0,
                left: 0
            };
            return jQuery.css(c, "position") === "fixed" ? b = c.getBoundingClientRect() : (a = this.offsetParent(), b = this.offset(), jQuery.nodeName(a[0], "html") || (d = a.offset()), d.top += jQuery.css(a[0], "borderTopWidth", !0), d.left += jQuery.css(a[0], "borderLeftWidth", !0)),
            {
                top: b.top - d.top - jQuery.css(c, "marginTop", !0),
                left: b.left - d.left - jQuery.css(c, "marginLeft", !0)
            }
        },
        offsetParent: function() {
            return this.map(function() {
                var a = this.offsetParent || docElem;
                while (a && !jQuery.nodeName(a, "html") && jQuery.css(a, "position") === "static") a = a.offsetParent;
                return a || docElem
            })
        }
    }),
    jQuery.each({
        scrollLeft: "pageXOffset",
        scrollTop: "pageYOffset"
    },
    function(a, b) {
        var c = "pageYOffset" === b;
        jQuery.fn[a] = function(d) {
            return jQuery.access(this,
            function(a, d, e) {
                var f = getWindow(a);
                if (e === undefined) return f ? f[b] : a[d];
                f ? f.scrollTo(c ? window.pageXOffset: e, c ? e: window.pageYOffset) : a[d] = e
            },
            a, d, arguments.length, null)
        }
    }),
    jQuery.each({
        Height: "height",
        Width: "width"
    },
    function(a, b) {
        jQuery.each({
            padding: "inner" + a,
            content: b,
            "": "outer" + a
        },
        function(c, d) {
            jQuery.fn[d] = function(d, e) {
                var f = arguments.length && (c || typeof d != "boolean"),
                g = c || (d === !0 || e === !0 ? "margin": "border");
                return jQuery.access(this,
                function(b, c, d) {
                    var e;
                    return jQuery.isWindow(b) ? b.document.documentElement["client" + a] : b.nodeType === 9 ? (e = b.documentElement, Math.max(b.body["scroll" + a], e["scroll" + a], b.body["offset" + a], e["offset" + a], e["client" + a])) : d === undefined ? jQuery.css(b, c, g) : jQuery.style(b, c, d, g)
                },
                b, f ? d: undefined, f, null)
            }
        })
    }),
    jQuery.fn.size = function() {
        return this.length
    },
    jQuery.fn.andSelf = jQuery.fn.addBack,
    typeof module == "object" && typeof module.exports == "object" ? module.exports = jQuery: typeof define == "function" && define.amd && define("jquery", [],
    function() {
        return jQuery
    }),
    typeof window == "object" && typeof window.document == "object" && (window.jQuery = window.$ = jQuery)
})(window),
jQuery.migrateMute === void 0 && (jQuery.migrateMute = !0),
function(a, b, c) {
    function d(c) {
        f[c] || (f[c] = !0, a.migrateWarnings.push(c), b.console && console.warn && !a.migrateMute && (console.warn("JQMIGRATE: " + c), a.migrateTrace && console.trace && console.trace()))
    }
    function e(b, e, f, g) {
        if (Object.defineProperty) try {
            return Object.defineProperty(b, e, {
                configurable: !0,
                enumerable: !0,
                get: function() {
                    return d(g),
                    f
                },
                set: function(a) {
                    d(g),
                    f = a
                }
            }),
            c
        } catch(h) {}
        a._definePropertyBroken = !0,
        b[e] = f
    }
    var f = {};
    a.migrateWarnings = [],
    !a.migrateMute && b.console && console.log && console.log("JQMIGRATE: Logging is active"),
    a.migrateTrace === c && (a.migrateTrace = !0),
    a.migrateReset = function() {
        f = {},
        a.migrateWarnings.length = 0
    },
    "BackCompat" === document.compatMode && d("jQuery is not compatible with Quirks Mode");
    var g = a("<input/>", {
        size: 1
    }).attr("size") && a.attrFn,
    h = a.attr,
    i = a.attrHooks.value && a.attrHooks.value.get ||
    function() {
        return null
    },
    j = a.attrHooks.value && a.attrHooks.value.set ||
    function() {
        return c
    },
    k = /^(?:input|button)$/i,
    l = /^[238]$/,
    m = /^(?:autofocus|autoplay|async|checked|controls|defer|disabled|hidden|loop|multiple|open|readonly|required|scoped|selected)$/i,
    n = /^(?:checked|selected)$/i;
    e(a, "attrFn", g || {},
    "jQuery.attrFn is deprecated"),
    a.attr = function(b, e, f, i) {
        var j = e.toLowerCase(),
        o = b && b.nodeType;
        return i && (4 > h.length && d("jQuery.fn.attr( props, pass ) is deprecated"), b && !l.test(o) && (g ? e in g: a.isFunction(a.fn[e]))) ? a(b)[e](f) : ("type" === e && f !== c && k.test(b.nodeName) && b.parentNode && d("Can't change the 'type' of an input or button in IE 6/7/8"), !a.attrHooks[j] && m.test(j) && (a.attrHooks[j] = {
            get: function(b, d) {
                var e, f = a.prop(b, d);
                return f === !0 || "boolean" != typeof f && (e = b.getAttributeNode(d)) && e.nodeValue !== !1 ? d.toLowerCase() : c
            },
            set: function(b, c, d) {
                var e;
                return c === !1 ? a.removeAttr(b, d) : (e = a.propFix[d] || d, e in b && (b[e] = !0), b.setAttribute(d, d.toLowerCase())),
                d
            }
        },
        n.test(j) && d("jQuery.fn.attr('" + j + "') may use property instead of attribute")), h.call(a, b, e, f))
    },
    a.attrHooks.value = {
        get: function(a, b) {
            var c = (a.nodeName || "").toLowerCase();
            return "button" === c ? i.apply(this, arguments) : ("input" !== c && "option" !== c && d("jQuery.fn.attr('value') no longer gets properties"), b in a ? a.value: null)
        },
        set: function(a, b) {
            var e = (a.nodeName || "").toLowerCase();
            return "button" === e ? j.apply(this, arguments) : ("input" !== e && "option" !== e && d("jQuery.fn.attr('value', val) no longer sets properties"), a.value = b, c)
        }
    };
    var o, p, q = a.fn.init,
    r = a.parseJSON,
    s = /^(?:[^<]*(<[\w\W]+>)[^>]*|#([\w\-]*))$/;
    a.fn.init = function(b, c, e) {
        var f;
        return b && "string" == typeof b && !a.isPlainObject(c) && (f = s.exec(b)) && f[1] && ("<" !== b.charAt(0) && d("$(html) HTML strings must start with '<' character"), c && c.context && (c = c.context), a.parseHTML) ? q.call(this, a.parseHTML(a.trim(b), c, !0), c, e) : q.apply(this, arguments)
    },
    a.fn.init.prototype = a.fn,
    a.parseJSON = function(a) {
        return a || null === a ? r.apply(this, arguments) : (d("jQuery.parseJSON requires a valid JSON string"), null)
    },
    a.uaMatch = function(a) {
        a = a.toLowerCase();
        var b = /(chrome)[ \/]([\w.]+)/.exec(a) || /(webkit)[ \/]([\w.]+)/.exec(a) || /(opera)(?:.*version|)[ \/]([\w.]+)/.exec(a) || /(msie) ([\w.]+)/.exec(a) || 0 > a.indexOf("compatible") && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec(a) || [];
        return {
            browser: b[1] || "",
            version: b[2] || "0"
        }
    },
    a.browser || (o = a.uaMatch(navigator.userAgent), p = {},
    o.browser && (p[o.browser] = !0, p.version = o.version), p.chrome ? p.webkit = !0 : p.webkit && (p.safari = !0), a.browser = p),
    e(a, "browser", a.browser, "jQuery.browser is deprecated"),
    a.sub = function() {
        function b(a, c) {
            return new b.fn.init(a, c)
        }
        a.extend(!0, b, this),
        b.superclass = this,
        b.fn = b.prototype = this(),
        b.fn.constructor = b,
        b.sub = this.sub,
        b.fn.init = function(d, e) {
            return e && e instanceof a && !(e instanceof b) && (e = b(e)),
            a.fn.init.call(this, d, e, c)
        },
        b.fn.init.prototype = b.fn;
        var c = b(document);
        return d("jQuery.sub() is deprecated"),
        b
    },
    a.ajaxSetup({
        converters: {
            "text json": a.parseJSON
        }
    });
    var t = a.fn.data;
    a.fn.data = function(b) {
        var e, f, g = this[0];
        return ! g || "events" !== b || 1 !== arguments.length || (e = a.data(g, b), f = a._data(g, b), e !== c && e !== f || f === c) ? t.apply(this, arguments) : (d("Use of jQuery.fn.data('events') is deprecated"), f)
    };
    var u = /\/(java|ecma)script/i,
    v = a.fn.andSelf || a.fn.addBack;
    a.fn.andSelf = function() {
        return d("jQuery.fn.andSelf() replaced by jQuery.fn.addBack()"),
        v.apply(this, arguments)
    },
    a.clean || (a.clean = function(b, e, f, g) {
        e = e || document,
        e = !e.nodeType && e[0] || e,
        e = e.ownerDocument || e,
        d("jQuery.clean() is deprecated");
        var h, i, j, k, l = [];
        if (a.merge(l, a.buildFragment(b, e).childNodes), f) for (j = function(a) {
            return ! a.type || u.test(a.type) ? g ? g.push(a.parentNode ? a.parentNode.removeChild(a) : a) : f.appendChild(a) : c
        },
        h = 0; null != (i = l[h]); h++) a.nodeName(i, "script") && j(i) || (f.appendChild(i), i.getElementsByTagName !== c && (k = a.grep(a.merge([], i.getElementsByTagName("script")), j), l.splice.apply(l, [h + 1, 0].concat(k)), h += k.length));
        return l
    });
    var w = a.event.add,
    x = a.event.remove,
    y = a.event.trigger,
    z = a.fn.toggle,
    A = a.fn.live,
    B = a.fn.die,
    C = "ajaxStart|ajaxStop|ajaxSend|ajaxComplete|ajaxError|ajaxSuccess",
    D = RegExp("\\b(?:" + C + ")\\b"),
    E = /(?:^|\s)hover(\.\S+|)\b/,
    F = function(b) {
        return "string" != typeof b || a.event.special.hover ? b: (E.test(b) && d("'hover' pseudo-event is deprecated, use 'mouseenter mouseleave'"), b && b.replace(E, "mouseenter$1 mouseleave$1"))
    };
    a.event.props && "attrChange" !== a.event.props[0] && a.event.props.unshift("attrChange", "attrName", "relatedNode", "srcElement"),
    a.event.dispatch && e(a.event, "handle", a.event.dispatch, "jQuery.event.handle is undocumented and deprecated"),
    a.event.add = function(a, b, c, e, f) {
        a !== document && D.test(b) && d("AJAX events should be attached to document: " + b),
        w.call(this, a, F(b || ""), c, e, f)
    },
    a.event.remove = function(a, b, c, d, e) {
        x.call(this, a, F(b) || "", c, d, e)
    },
    a.fn.error = function() {
        var a = Array.prototype.slice.call(arguments, 0);
        return d("jQuery.fn.error() is deprecated"),
        a.splice(0, 0, "error"),
        arguments.length ? this.bind.apply(this, a) : (this.triggerHandler.apply(this, a), this)
    },
    a.fn.toggle = function(b, c) {
        if (!a.isFunction(b) || !a.isFunction(c)) return z.apply(this, arguments);
        d("jQuery.fn.toggle(handler, handler...) is deprecated");
        var e = arguments,
        f = b.guid || a.guid++,
        g = 0,
        h = function(c) {
            var d = (a._data(this, "lastToggle" + b.guid) || 0) % g;
            return a._data(this, "lastToggle" + b.guid, d + 1),
            c.preventDefault(),
            e[d].apply(this, arguments) || !1
        };
        for (h.guid = f; e.length > g;) e[g++].guid = f;
        return this.click(h)
    },
    a.fn.live = function(b, c, e) {
        return d("jQuery.fn.live() is deprecated"),
        A ? A.apply(this, arguments) : (a(this.context).on(b, this.selector, c, e), this)
    },
    a.fn.die = function(b, c) {
        return d("jQuery.fn.die() is deprecated"),
        B ? B.apply(this, arguments) : (a(this.context).off(b, this.selector || "**", c), this)
    },
    a.event.trigger = function(a, b, c, e) {
        return c || D.test(a) || d("Global events are undocumented and deprecated"),
        y.call(this, a, b, c || document, e)
    },
    a.each(C.split("|"),
    function(b, c) {
        a.event.special[c] = {
            setup: function() {
                var b = this;
                return b !== document && (a.event.add(document, c + "." + a.guid,
                function() {
                    a.event.trigger(c, null, b, !0)
                }), a._data(this, c, a.guid++)),
                !1
            },
            teardown: function() {
                return this !== document && a.event.remove(document, c + "." + a._data(this, c)),
                !1
            }
        }
    })
} (jQuery, window),
function(a, b) {
    var c = function() {
        var b = a._data(document, "events");
        return b && b.click && a.grep(b.click,
        function(a) {
            return a.namespace === "rails"
        }).length
    };
    c() && a.error("jquery-ujs has already been loaded!");
    var d;
    a.rails = d = {
        linkClickSelector: "a[data-confirm], a[data-method], a[data-remote], a[data-disable-with]",
        inputChangeSelector: "select[data-remote], input[data-remote], textarea[data-remote]",
        formSubmitSelector: "form",
        formInputClickSelector: "form input[type=submit], form input[type=image], form button[type=submit], form button:not([type])",
        disableSelector: "input[data-disable-with], button[data-disable-with], textarea[data-disable-with]",
        enableSelector: "input[data-disable-with]:disabled, button[data-disable-with]:disabled, textarea[data-disable-with]:disabled",
        requiredInputSelector: "input[name][required]:not([disabled]),textarea[name][required]:not([disabled])",
        fileInputSelector: "input:file",
        linkDisableSelector: "a[data-disable-with]",
        CSRFProtection: function(b) {
            var c = a('meta[name="csrf-token"]').attr("content");
            c && b.setRequestHeader("X-CSRF-Token", c)
        },
        fire: function(b, c, d) {
            var e = a.Event(c);
            return b.trigger(e, d),
            e.result !== !1
        },
        confirm: function(a) {
            return confirm(a)
        },
        ajax: function(b) {
            return a.ajax(b)
        },
        href: function(a) {
            return a.attr("href")
        },
        handleRemote: function(c) {
            var e, f, g, h, i, j, k, l;
            if (d.fire(c, "ajax:before")) {
                h = c.data("cross-domain"),
                i = h === b ? null: h,
                j = c.data("with-credentials") || null,
                k = c.data("type") || a.ajaxSettings && a.ajaxSettings.dataType;
                if (c.is("form")) {
                    e = c.attr("method"),
                    f = c.attr("action"),
                    g = c.serializeArray(),
                    a.each(a.ajaxSettings.data,
                    function(a, b) {
                        g.push({
                            name: a,
                            value: b
                        })
                    });
                    var m = c.data("ujs:submit-button");
                    m && (g.push(m), c.data("ujs:submit-button", null))
                } else c.is(d.inputChangeSelector) ? (e = c.data("method"), f = c.data("url"), g = c.serializeArray(), a.each(a.ajaxSettings.data,
                function(a, b) {
                    g.push({
                        name: a,
                        value: b
                    })
                }), c.data("params") && a.each(mcw.parseParams(c.data("params")),
                function(a, b) {
                    g.push({
                        name: a,
                        value: b
                    })
                })) : (e = c.data("method"), f = d.href(c), g = mcw.parseParams(c.data("params")) || {});
                l = {
                    type: e || "GET",
                    data: g,
                    dataType: k,
                    beforeSend: function(a, e) {
                        return e.dataType === b && a.setRequestHeader("accept", "*/*;q=0.5, " + e.accepts.script),
                        d.fire(c, "ajax:beforeSend", [a, e])
                    },
                    success: function(a, b, d) {
                        c.trigger("ajax:success", [a, b, d])
                    },
                    complete: function(a, b) {
                        c.trigger("ajax:complete", [a, b])
                    },
                    error: function(a, b, d) {
                        c.trigger("ajax:error", [a, b, d])
                    },
                    xhrFields: {
                        withCredentials: j
                    },
                    crossDomain: i
                },
                f && (l.url = f);
                var n = d.ajax(l);
                return c.trigger("ajax:send", n),
                n
            }
            return ! 1
        },
        handleMethod: function(c) {
            var e = d.href(c),
            f = c.data("method"),
            g = c.attr("target"),
            h = a("meta[name=csrf-token]").attr("content"),
            i = a("meta[name=csrf-param]").attr("content"),
            j = a('<form method="post" action="' + e + '"></form>'),
            k = '<input name="_method" value="' + f + '" type="hidden" />';
            i !== b && h !== b && (k += '<input name="' + i + '" value="' + h + '" type="hidden" />'),
            g && j.attr("target", g),
            j.hide().append(k).appendTo("body"),
            j.submit()
        },
        disableFormElements: function(b) {
            b.find(d.disableSelector).each(function() {
                var b = a(this),
                c = b.is("button") ? "html": "val";
                b.data("ujs:enable-with", b[c]()),
                b[c](b.data("disable-with")),
                b.prop("disabled", !0)
            })
        },
        enableFormElements: function(b) {
            b.find(d.enableSelector).each(function() {
                var b = a(this),
                c = b.is("button") ? "html": "val";
                b.data("ujs:enable-with") && b[c](b.data("ujs:enable-with")),
                b.prop("disabled", !1)
            })
        },
        allowAction: function(a, b) {
            var c = a.data("confirm"),
            e = !1,
            b;
            return c ? (d.fire(a, "confirm", [b]) && mcw.confirm({
                msg: c.replace("\\n", "<br>"),
                callback: function(c, f) {
                    if (!c) return;
                    d.fire(a, "confirm:complete", [e]) && b()
                }
            }), !1) : !0
        },
        blankInputs: function(b, c, d) {
            var e = a(),
            f,
            g,
            h = c || "input,textarea",
            i = b.find(h);
            return i.each(function() {
                f = a(this),
                g = f.is(":checkbox,:radio") ? f.is(":checked") : f.val();
                if (!g == !d) {
                    if (f.is(":radio") && i.filter('input:radio:checked[name="' + f.attr("name") + '"]').length) return ! 0;
                    e = e.add(f)
                }
            }),
            e.length ? e: !1
        },
        nonBlankInputs: function(a, b) {
            return d.blankInputs(a, b, !0)
        },
        stopEverything: function(b) {
            return a(b.target).trigger("ujs:everythingStopped"),
            b.stopImmediatePropagation(),
            !1
        },
        callFormSubmitBindings: function(c, d) {
            var e = c.data("events"),
            f = !0;
            return e !== b && e.submit !== b && a.each(e.submit,
            function(a, b) {
                if (typeof b.handler == "function") return f = b.handler(d)
            }),
            f
        },
        disableElement: function(a) {
            a.data("ujs:enable-with", a.html()),
            a.html(a.data("disable-with")),
            a.bind("click.railsDisable",
            function(a) {
                return d.stopEverything(a)
            })
        },
        enableElement: function(a) {
            a.data("ujs:enable-with") !== b && (a.html(a.data("ujs:enable-with")), a.data("ujs:enable-with", !1)),
            a.unbind("click.railsDisable")
        }
    },
    d.fire(a(document), "rails:attachBindings") && (a.ajaxPrefilter(function(a, b, c) {
        a.crossDomain || d.CSRFProtection(c)
    }), a(document).delegate(d.linkDisableSelector, "ajax:complete",
    function() {
        d.enableElement(a(this))
    }), a(document).delegate(d.linkClickSelector, "click.rails",
    function(c) {
        function h() {
            e.is(d.linkDisableSelector) && d.disableElement(e);
            if (e.data("remote") !== b) {
                if ((c.metaKey || c.ctrlKey) && (!f || f === "GET") && !g) return ! 0;
                var a = d.handleRemote(e);
                return a === !1 ? d.enableElement(e) : a.error(function() {
                    d.enableElement(e)
                }),
                !1
            }
            if (e.data("method")) return d.handleMethod(e),
            !1
        }
        var e = a(this),
        f = e.data("method"),
        g = e.data("params");
        return d.allowAction(e, h) ? h() : d.stopEverything(c)
    }), a(document).delegate(d.inputChangeSelector, "change.rails",
    function(b) {
        function e() {
            return d.handleRemote(c),
            !1
        }
        var c = a(this);
        return d.allowAction(c, e) ? e() : d.stopEverything(b)
    }), a(document).delegate(d.formSubmitSelector, "submit.rails",
    function(c) {
        function i() {
            if (g && e.attr("novalidate") == b && d.fire(e, "ajax:aborted:required", [g])) return d.stopEverything(c);
            if (f) {
                if (h) {
                    setTimeout(function() {
                        d.disableFormElements(e)
                    },
                    13);
                    var i = d.fire(e, "ajax:aborted:file", [h]);
                    return i || setTimeout(function() {
                        d.enableFormElements(e)
                    },
                    13),
                    i
                }
                return ! a.support.submitBubbles && a().jquery < "1.7" && d.callFormSubmitBindings(e, c) === !1 ? d.stopEverything(c) : (d.handleRemote(e), !1)
            }
            setTimeout(function() {
                d.disableFormElements(e)
            },
            13)
        }
        var e = a(this),
        f = e.data("remote") !== b,
        g = d.blankInputs(e, d.requiredInputSelector),
        h = d.nonBlankInputs(e, d.fileInputSelector);
        return d.allowAction(e, i) ? i() : d.stopEverything(c)
    }), a(document).delegate(d.formInputClickSelector, "click.rails",
    function(b) {
        function e() {
            var a = c.attr("name"),
            b = a ? {
                name: a,
                value: c.val()
            }: null;
            c.closest("form").data("ujs:submit-button", b)
        }
        var c = a(this);
        return d.allowAction(c, e) ? e() : d.stopEverything(b)
    }), a(document).delegate(d.formSubmitSelector, "ajax:beforeSend.rails",
    function(b) {
        this == b.target && d.disableFormElements(a(this))
    }), a(document).delegate(d.formSubmitSelector, "ajax:complete.rails",
    function(b) {
        this == b.target && d.enableFormElements(a(this))
    }), a(function() {
        csrf_token = a("meta[name=csrf-token]").attr("content"),
        csrf_param = a("meta[name=csrf-param]").attr("content"),
        a('form input[name="' + csrf_param + '"]').val(csrf_token)
    }))
} (jQuery),
function(a, b, c) {
    function j(a) {
        var b = {},
        d = /^jQuery\d+$/;
        return c.each(a.attributes,
        function(a, c) {
            c.specified && !d.test(c.name) && (b[c.name] = c.value)
        }),
        b
    }
    function k(a, d) {
        var e = this,
        f = c(e);
        if (e.value == f.attr("placeholder") && f.hasClass("placeholder")) if (f.data("placeholder-password")) {
            f = f.hide().next().show().attr("id", f.removeAttr("id").data("placeholder-id"));
            if (a === !0) return f[0].value = d;
            f.focus()
        } else e.value = "",
        f.removeClass("placeholder"),
        e == b.activeElement && e.select()
    }
    function l() {
        var a, b = this,
        d = c(b),
        e = d,
        f = this.id;
        if (b.value == "") {
            if (b.type == "password") {
                if (!d.data("placeholder-textinput")) {
                    try {
                        a = d.clone().attr({
                            type: "text"
                        })
                    } catch(g) {
                        a = c("<input>").attr(c.extend(j(this), {
                            type: "text"
                        }))
                    }
                    a.removeAttr("name").data({
                        "placeholder-password": !0,
                        "placeholder-id": f
                    }).bind("focus.placeholder", k),
                    d.data({
                        "placeholder-textinput": a,
                        "placeholder-id": f
                    }).before(a)
                }
                d = d.removeAttr("id").hide().prev().attr("id", f).show()
            }
            d.addClass("placeholder"),
            d[0].value = d.attr("placeholder")
        } else d.removeClass("placeholder")
    }
    var d = "placeholder" in b.createElement("input"),
    e = "placeholder" in b.createElement("textarea"),
    f = c.fn,
    g = c.valHooks,
    h,
    i;
    d && e ? (i = f.placeholder = function() {
        return this
    },
    i.input = i.textarea = !0) : (i = f.placeholder = function() {
        var a = this;
        return a.filter((d ? "textarea": ":input") + "[placeholder]").not(".placeholder").bind({
            "focus.placeholder": k,
            "blur.placeholder": l
        }).data("placeholder-enabled", !0).trigger("blur.placeholder"),
        a
    },
    i.input = d, i.textarea = e, h = {
        get: function(a) {
            var b = c(a);
            return b.data("placeholder-enabled") && b.hasClass("placeholder") ? "": a.value
        },
        set: function(a, d) {
            var e = c(a);
            return e.data("placeholder-enabled") ? (d == "" ? (a.value = d, a != b.activeElement && l.call(a)) : e.hasClass("placeholder") ? k.call(a, !0, d) || (a.value = d) : a.value = d, e) : a.value = d
        }
    },
    d || (g.input = h), e || (g.textarea = h), c(function() {
        c(b).delegate("form", "submit.placeholder",
        function() {
            var a = c(".placeholder", this).each(k);
            setTimeout(function() {
                a.each(l)
            },
            10)
        })
    }), c(a).bind("beforeunload.placeholder",
    function() {
        c(".placeholder").each(function() {
            this.value = ""
        })
    }))
} (this, document, jQuery),
function(window, undefined) {
    function returnTrue() {
        return ! 0
    }
    function returnFalse() {
        return ! 1
    }
    var document = window.document;
    document.createElement("video"),
    document.createElement("audio");
    var VideoJS = function(a, b, c) {
        var d;
        if (typeof a == "string") {
            a.indexOf("#") === 0 && (a = a.slice(1));
            if (_V_.players[a]) return _V_.players[a];
            d = _V_.el(a)
        } else d = a;
        if (!d || !d.nodeName) throw new TypeError("The element or ID supplied is not valid. (VideoJS)");
        return d.player || new _V_.Player(d, b, c)
    },
    _V_ = VideoJS,
    CDN_VERSION = "3.2";
    VideoJS.players = {},
    VideoJS.options = {
        techOrder: ["html5", "flash"],
        html5: {},
        flash: {
            swf: "http://vjs.zencdn.net/c/video-js.swf"
        },
        width: "auto",
        height: "auto",
        defaultVolume: 0,
        components: {
            posterImage: {},
            textTrackDisplay: {},
            loadingSpinner: {},
            bigPlayButton: {},
            controlBar: {}
        }
    },
    CDN_VERSION != "GENERATED_CDN_VSN" && (_V_.options.flash.swf = "http://vjs.zencdn.net/" + CDN_VERSION + "/video-js.swf"),
    _V_.merge = function(a, b, c) {
        b || (b = {});
        for (var d in b) b.hasOwnProperty(d) && (!c || !a.hasOwnProperty(d)) && (a[d] = b[d]);
        return a
    },
    _V_.extend = function(a) {
        this.merge(this, a, !0)
    },
    _V_.extend({
        tech: {},
        controlSets: {},
        isIE: function() {
            return ! 1
        },
        isFF: function() {
            return !! _V_.ua.match("Firefox")
        },
        isIPad: function() {
            return navigator.userAgent.match(/iPad/i) !== null
        },
        isIPhone: function() {
            return navigator.userAgent.match(/iPhone/i) !== null
        },
        isIOS: function() {
            return VideoJS.isIPhone() || VideoJS.isIPad()
        },
        iOSVersion: function() {
            var a = navigator.userAgent.match(/OS (\d+)_/i);
            if (a && a[1]) return a[1]
        },
        isAndroid: function() {
            return navigator.userAgent.match(/Android.*AppleWebKit/i) !== null
        },
        androidVersion: function() {
            var a = navigator.userAgent.match(/Android (\d+)\./i);
            if (a && a[1]) return a[1]
        },
        testVid: document.createElement("video"),
        ua: navigator.userAgent,
        support: {},
        each: function(a, b) {
            if (!a || a.length === 0) return;
            for (var c = 0, d = a.length; c < d; c++) b.call(this, a[c], c)
        },
        eachProp: function(a, b) {
            if (!a) return;
            for (var c in a) a.hasOwnProperty(c) && b.call(this, c, a[c])
        },
        el: function(a) {
            return document.getElementById(a)
        },
        createElement: function(a, b) {
            var c = document.createElement(a),
            d;
            for (d in b) b.hasOwnProperty(d) && (d.indexOf("-") !== -1 ? c.setAttribute(d, b[d]) : c[d] = b[d]);
            return c
        },
        insertFirst: function(a, b) {
            b.firstChild ? b.insertBefore(a, b.firstChild) : b.appendChild(a)
        },
        addClass: function(a, b) { (" " + a.className + " ").indexOf(" " + b + " ") == -1 && (a.className = a.className === "" ? b: a.className + " " + b)
        },
        removeClass: function(a, b) {
            if (a.className.indexOf(b) == -1) return;
            var c = a.className.split(" ");
            c.splice(c.indexOf(b), 1),
            a.className = c.join(" ")
        },
        remove: function(a, b) {
            if (!b) return;
            var c = b.indexOf(a);
            if (c != -1) return b.splice(c, 1)
        },
        blockTextSelection: function() {
            document.body.focus(),
            document.onselectstart = function() {
                return ! 1
            }
        },
        unblockTextSelection: function() {
            document.onselectstart = function() {
                return ! 0
            }
        },
        formatTime: function(a, b) {
            b = b || a;
            var c = Math.floor(a % 60),
            d = Math.floor(a / 60 % 60),
            e = Math.floor(a / 3600),
            f = Math.floor(b / 60 % 60),
            g = Math.floor(b / 3600);
            return e = e > 0 || g > 0 ? e + ":": "",
            d = ((e || f >= 10) && d < 10 ? "0" + d: d) + ":",
            c = c < 10 ? "0" + c: c,
            e + d + c
        },
        uc: function(a) {
            return a.charAt(0).toUpperCase() + a.slice(1)
        },
        getRelativePosition: function(a, b) {
            return Math.max(0, Math.min(1, (a - _V_.findPosX(b)) / b.offsetWidth))
        },
        getComputedStyleValue: function(a, b) {
            return window.getComputedStyle(a, null).getPropertyValue(b)
        },
        trim: function(a) {
            return a.toString().replace(/^\s+/, "").replace(/\s+$/, "")
        },
        round: function(a, b) {
            return b || (b = 0),
            Math.round(a * Math.pow(10, b)) / Math.pow(10, b)
        },
        isEmpty: function(a) {
            for (var b in a) return ! 1;
            return ! 0
        },
        createTimeRange: function(a, b) {
            return {
                length: 1,
                start: function() {
                    return a
                },
                end: function() {
                    return b
                }
            }
        },
        cache: {},
        guid: 1,
        expando: "vdata" + (new Date).getTime(),
        getData: function(a) {
            var b = a[_V_.expando];
            return b || (b = a[_V_.expando] = _V_.guid++, _V_.cache[b] = {}),
            _V_.cache[b]
        },
        removeData: function(a) {
            var b = a[_V_.expando];
            if (!b) return;
            delete _V_.cache[b];
            try {
                delete a[_V_.expando]
            } catch(c) {
                a.removeAttribute ? a.removeAttribute(_V_.expando) : a[_V_.expando] = null
            }
        },
        proxy: function(a, b, c) {
            b.guid || (b.guid = _V_.guid++);
            var d = function() {
                return b.apply(a, arguments)
            };
            return d.guid = c ? c + "_" + b.guid: b.guid,
            d
        },
        get: function(a, b, c) {
            var d = a.indexOf("file:") == 0 || window.location.href.indexOf("file:") == 0 && a.indexOf("http:") == -1;
            typeof XMLHttpRequest == "undefined" && (XMLHttpRequest = function() {
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP.6.0")
                } catch(a) {}
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP.3.0")
                } catch(b) {}
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP")
                } catch(c) {}
                throw new Error("This browser does not support XMLHttpRequest.")
            });
            var e = new XMLHttpRequest;
            try {
                e.open("GET", a)
            } catch(f) {
                return _V_.log("VideoJS XMLHttpRequest (open)", f),
                !1
            }
            e.onreadystatechange = _V_.proxy(this,
            function() {
                e.readyState == 4 && (e.status == 200 || d && e.status == 0 ? b(e.responseText) : c && c())
            });
            try {
                e.send()
            } catch(f) {
                _V_.log("VideoJS XMLHttpRequest (send)", f),
                c && c(f)
            }
        },
        setLocalStorage: function(a, b) {
            var c = window.localStorage || !1;
            if (!c) return;
            try {
                c[a] = b
            } catch(d) {
                d.code == 22 || d.code == 1014 ? _V_.log("LocalStorage Full (VideoJS)", d) : _V_.log("LocalStorage Error (VideoJS)", d)
            }
        },
        getAbsoluteURL: function(a) {
            return a.match(/^https?:\/\//) || (a = _V_.createElement("div", {
                innerHTML: '<a href="' + a + '">x</a>'
            }).firstChild.href),
            a
        }
    }),
    _V_.log = function() {
        _V_.log.history = _V_.log.history || [],
        _V_.log.history.push(arguments);
        if (window.console) {
            arguments.callee = arguments.callee.caller;
            var a = [].slice.call(arguments);
            typeof console.log == "object" ? _V_.log.apply.call(console.log, console, a) : console.log.apply(console, a)
        }
    },
    function(a) {
        function b() {}
        for (var c = "assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","), d; d = c.pop();) a[d] = a[d] || b
    } (function() {
        try {
            return console.log(),
            window.console
        } catch(a) {
            return window.console = {}
        }
    } ()),
    "getBoundingClientRect" in document.documentElement ? _V_.findPosX = function(a) {
        var b;
        try {
            b = a.getBoundingClientRect()
        } catch(c) {}
        if (!b) return 0;
        var d = document.documentElement,
        e = document.body,
        f = d.clientLeft || e.clientLeft || 0,
        g = window.pageXOffset || e.scrollLeft,
        h = b.left + g - f;
        return h
    }: _V_.findPosX = function(a) {
        var b = a.offsetLeft;
        while (a = obj.offsetParent) a.className.indexOf("video-js") != -1,
        b += a.offsetLeft;
        return b
    },
    function() {
        var a = !1,
        b = /xyz/.test(function() {
            xyz
        }) ? /\b_super\b/: /.*/;
        _V_.Class = function() {},
        _V_.Class.extend = function(c) {
            function g() {
                if (!a && this.init) return this.init.apply(this, arguments);
                if (!a) return arguments.callee.prototype.init()
            }
            var d = this.prototype;
            a = !0;
            var e = new this;
            a = !1;
            for (var f in c) e[f] = typeof c[f] == "function" && typeof d[f] == "function" && b.test(c[f]) ?
            function(a, b) {
                return function() {
                    var c = this._super;
                    this._super = d[a];
                    var e = b.apply(this, arguments);
                    return this._super = c,
                    e
                }
            } (f, c[f]) : c[f];
            return g.prototype = e,
            g.constructor = g,
            g.extend = arguments.callee,
            g
        }
    } (),
    _V_.Component = _V_.Class.extend({
        init: function(a, b) {
            this.player = a,
            b = this.options = _V_.merge(this.options || {},
            b),
            b.el ? this.el = b.el: this.el = this.createElement(),
            this.initComponents()
        },
        destroy: function() {},
        createElement: function(a, b) {
            return _V_.createElement(a || "div", b)
        },
        buildCSSClass: function() {
            return ""
        },
        initComponents: function() {
            var a = this.options;
            a && a.components && this.eachProp(a.components,
            function(a, b) {
                var c = this.proxy(function() {
                    this[a] = this.addComponent(a, b)
                });
                b.loadEvent ? this.one(b.loadEvent, c) : c()
            })
        },
        addComponent: function(a, b) {
            var c, d;
            return typeof a == "string" ? (b = b || {},
            d = b.componentClass || _V_.uc(a), c = new _V_[d](this.player || this, b)) : c = a,
            this.el.appendChild(c.el),
            c
        },
        removeComponent: function(a) {
            this.el.removeChild(a.el)
        },
        show: function() {
            this.el.style.display = "block"
        },
        hide: function() {
            this.el.style.display = "none"
        },
        fadeIn: function() {
            this.removeClass("vjs-fade-out"),
            this.addClass("vjs-fade-in")
        },
        fadeOut: function() {
            this.removeClass("vjs-fade-in"),
            this.addClass("vjs-fade-out")
        },
        lockShowing: function() {
            var a = this.el.style;
            a.display = "block",
            a.opacity = 1,
            a.visiblity = "visible"
        },
        unlockShowing: function() {
            var a = this.el.style;
            a.display = "",
            a.opacity = "",
            a.visiblity = ""
        },
        addClass: function(a) {
            _V_.addClass(this.el, a)
        },
        removeClass: function(a) {
            _V_.removeClass(this.el, a)
        },
        addEvent: function(a, b, c) {
            return _V_.addEvent(this.el, a, _V_.proxy(this, b))
        },
        removeEvent: function(a, b) {
            return _V_.removeEvent(this.el, a, b)
        },
        triggerEvent: function(a, b) {
            return _V_.triggerEvent(this.el, a, b)
        },
        one: function(a, b) {
            _V_.one(this.el, a, _V_.proxy(this, b))
        },
        ready: function(a) {
            return a ? (this.isReady ? a.call(this) : (this.readyQueue === undefined && (this.readyQueue = []), this.readyQueue.push(a)), this) : this
        },
        triggerReady: function() {
            this.isReady = !0,
            this.readyQueue && this.readyQueue.length > 0 && (this.each(this.readyQueue,
            function(a) {
                a.call(this)
            }), this.readyQueue = [], this.triggerEvent("ready"))
        },
        each: function(a, b) {
            _V_.each.call(this, a, b)
        },
        eachProp: function(a, b) {
            _V_.eachProp.call(this, a, b)
        },
        extend: function(a) {
            _V_.merge(this, a)
        },
        proxy: function(a, b) {
            return _V_.proxy(this, a, b)
        }
    }),
    _V_.Control = _V_.Component.extend({
        buildCSSClass: function() {
            return "vjs-control " + this._super()
        }
    }),
    _V_.ControlBar = _V_.Component.extend({
        options: {
            loadEvent: "play",
            components: {
                playToggle: {},
                fullscreenToggle: {},
                currentTimeDisplay: {},
                timeDivider: {},
                durationDisplay: {},
                remainingTimeDisplay: {},
                progressControl: {},
                volumeControl: {},
                muteToggle: {}
            }
        },
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("play", this.proxy(function() {
                this.fadeIn(),
                this.player.addEvent("mouseover", this.proxy(this.fadeIn)),
                this.player.addEvent("mouseout", this.proxy(this.fadeOut))
            }))
        },
        createElement: function() {
            return _V_.createElement("div", {
                className: "vjs-controls"
            })
        },
        fadeIn: function() {
            this._super(),
            this.player.triggerEvent("controlsvisible")
        },
        fadeOut: function() {
            this._super(),
            this.player.triggerEvent("controlshidden")
        },
        lockShowing: function() {
            this.el.style.opacity = "1"
        }
    }),
    _V_.Button = _V_.Control.extend({
        init: function(a, b) {
            this._super(a, b),
            this.addEvent("click", this.onClick),
            this.addEvent("focus", this.onFocus),
            this.addEvent("blur", this.onBlur)
        },
        createElement: function(a, b) {
            return b = _V_.merge({
                className: this.buildCSSClass(),
                innerHTML: '<div><span class="vjs-control-text">' + (this.buttonText || "Need Text") + "</span></div>",
                role: "button",
                tabIndex: 0
            },
            b),
            this._super(a, b)
        },
        onClick: function() {},
        onFocus: function() {
            _V_.addEvent(document, "keyup", _V_.proxy(this, this.onKeyPress))
        },
        onKeyPress: function(a) {
            if (a.which == 32 || a.which == 13) a.preventDefault(),
            this.onClick()
        },
        onBlur: function() {
            _V_.removeEvent(document, "keyup", _V_.proxy(this, this.onKeyPress))
        }
    }),
    _V_.PlayButton = _V_.Button.extend({
        buttonText: "Play",
        buildCSSClass: function() {
            return "vjs-play-button " + this._super()
        },
        onClick: function() {
            this.player.play()
        }
    }),
    _V_.PauseButton = _V_.Button.extend({
        buttonText: "Pause",
        buildCSSClass: function() {
            return "vjs-pause-button " + this._super()
        },
        onClick: function() {
            this.player.pause()
        }
    }),
    _V_.PlayToggle = _V_.Button.extend({
        buttonText: "Play",
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("play", _V_.proxy(this, this.onPlay)),
            a.addEvent("pause", _V_.proxy(this, this.onPause))
        },
        buildCSSClass: function() {
            return "vjs-play-control " + this._super()
        },
        onClick: function() {
            this.player.paused() ? this.player.play() : this.player.pause()
        },
        onPlay: function() {
            _V_.removeClass(this.el, "vjs-paused"),
            _V_.addClass(this.el, "vjs-playing")
        },
        onPause: function() {
            _V_.removeClass(this.el, "vjs-playing"),
            _V_.addClass(this.el, "vjs-paused")
        }
    }),
    _V_.FullscreenToggle = _V_.Button.extend({
        buttonText: "Fullscreen",
        buildCSSClass: function() {
            return "vjs-fullscreen-control " + this._super()
        },
        onClick: function() {
            this.player.isFullScreen ? this.player.cancelFullScreen() : this.player.requestFullScreen()
        }
    }),
    _V_.BigPlayButton = _V_.Button.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("play", _V_.proxy(this, this.hide)),
            a.addEvent("ended", _V_.proxy(this, this.show))
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-big-play-button",
                innerHTML: "<span></span>"
            })
        },
        onClick: function() {
            this.player.currentTime() && this.player.currentTime(0),
            this.player.play()
        }
    }),
    _V_.LoadingSpinner = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("canplay", _V_.proxy(this, this.hide)),
            a.addEvent("canplaythrough", _V_.proxy(this, this.hide)),
            a.addEvent("playing", _V_.proxy(this, this.hide)),
            a.addEvent("seeking", _V_.proxy(this, this.show)),
            a.addEvent("error", _V_.proxy(this, this.show)),
            a.addEvent("waiting", _V_.proxy(this, this.show))
        },
        createElement: function() {
            var a, b;
            return typeof this.player.el.style.WebkitBorderRadius == "string" || typeof this.player.el.style.MozBorderRadius == "string" || typeof this.player.el.style.KhtmlBorderRadius == "string" || typeof this.player.el.style.borderRadius == "string" ? (a = "vjs-loading-spinner", b = "<div class='ball1'></div><div class='ball2'></div><div class='ball3'></div><div class='ball4'></div><div class='ball5'></div><div class='ball6'></div><div class='ball7'></div><div class='ball8'></div>") : (a = "vjs-loading-spinner-fallback", b = ""),
            this._super("div", {
                className: a,
                innerHTML: b
            })
        }
    }),
    _V_.CurrentTimeDisplay = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("timeupdate", _V_.proxy(this, this.updateContent))
        },
        createElement: function() {
            var a = this._super("div", {
                className: "vjs-current-time vjs-time-controls vjs-control"
            });
            return this.content = _V_.createElement("div", {
                className: "vjs-current-time-display",
                innerHTML: "0:00"
            }),
            a.appendChild(_V_.createElement("div").appendChild(this.content)),
            a
        },
        updateContent: function() {
            var a = this.player.scrubbing ? this.player.values.currentTime: this.player.currentTime();
            this.content.innerHTML = _V_.formatTime(a, this.player.duration())
        }
    }),
    _V_.DurationDisplay = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("timeupdate", _V_.proxy(this, this.updateContent))
        },
        createElement: function() {
            var a = this._super("div", {
                className: "vjs-duration vjs-time-controls vjs-control"
            });
            return this.content = _V_.createElement("div", {
                className: "vjs-duration-display",
                innerHTML: "0:00"
            }),
            a.appendChild(_V_.createElement("div").appendChild(this.content)),
            a
        },
        updateContent: function() {
            this.player.duration() && (this.content.innerHTML = _V_.formatTime(this.player.duration()))
        }
    }),
    _V_.TimeDivider = _V_.Component.extend({
        createElement: function() {
            return this._super("div", {
                className: "vjs-time-divider",
                innerHTML: "<div><span>/</span></div>"
            })
        }
    }),
    _V_.RemainingTimeDisplay = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("timeupdate", _V_.proxy(this, this.updateContent))
        },
        createElement: function() {
            var a = this._super("div", {
                className: "vjs-remaining-time vjs-time-controls vjs-control"
            });
            return this.content = _V_.createElement("div", {
                className: "vjs-remaining-time-display",
                innerHTML: "-0:00"
            }),
            a.appendChild(_V_.createElement("div").appendChild(this.content)),
            a
        },
        updateContent: function() {
            this.player.duration() && (this.content.innerHTML = "-" + _V_.formatTime(this.player.remainingTime()))
        }
    }),
    _V_.Slider = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent(this.playerEvent, _V_.proxy(this, this.update)),
            this.addEvent("mousedown", this.onMouseDown),
            this.addEvent("focus", this.onFocus),
            this.addEvent("blur", this.onBlur),
            this.player.addEvent("controlsvisible", this.proxy(this.update)),
            this.update()
        },
        createElement: function(a, b) {
            return b = _V_.merge({
                role: "slider",
                "aria-valuenow": 0,
                "aria-valuemin": 0,
                "aria-valuemax": 100,
                tabIndex: 0
            },
            b),
            this._super(a, b)
        },
        onMouseDown: function(a) {
            a.preventDefault(),
            _V_.blockTextSelection(),
            _V_.addEvent(document, "mousemove", _V_.proxy(this, this.onMouseMove)),
            _V_.addEvent(document, "mouseup", _V_.proxy(this, this.onMouseUp)),
            this.onMouseMove(a)
        },
        onMouseUp: function(a) {
            _V_.unblockTextSelection(),
            _V_.removeEvent(document, "mousemove", this.onMouseMove, !1),
            _V_.removeEvent(document, "mouseup", this.onMouseUp, !1),
            this.update()
        },
        update: function() {
            var a, b = this.getPercent();
            handle = this.handle,
            bar = this.bar,
            isNaN(b) && (b = 0),
            a = b;
            if (handle) {
                var c = this.el,
                d = c.offsetWidth,
                e = handle.el.offsetWidth,
                f = e ? e / d: 0,
                g = 1 - f;
                adjustedProgress = b * g,
                a = adjustedProgress + f / 2,
                handle.el.style.left = _V_.round(adjustedProgress * 100, 2) + "%"
            }
            bar.el.style.width = _V_.round(a * 100, 2) + "%"
        },
        calculateDistance: function(a) {
            var b = this.el,
            c = _V_.findPosX(b),
            d = b.offsetWidth,
            e = this.handle;
            if (e) {
                var f = e.el.offsetWidth;
                c += f / 2,
                d -= f
            }
            return Math.max(0, Math.min(1, (a.pageX - c) / d))
        },
        onFocus: function(a) {
            _V_.addEvent(document, "keyup", _V_.proxy(this, this.onKeyPress))
        },
        onKeyPress: function(a) {
            a.which == 37 ? (a.preventDefault(), this.stepBack()) : a.which == 39 && (a.preventDefault(), this.stepForward())
        },
        onBlur: function(a) {
            _V_.removeEvent(document, "keyup", _V_.proxy(this, this.onKeyPress))
        }
    }),
    _V_.ProgressControl = _V_.Component.extend({
        options: {
            components: {
                seekBar: {}
            }
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-progress-control vjs-control"
            })
        }
    }),
    _V_.SeekBar = _V_.Slider.extend({
        options: {
            components: {
                loadProgressBar: {},
                bar: {
                    componentClass: "PlayProgressBar"
                },
                handle: {
                    componentClass: "SeekHandle"
                }
            }
        },
        playerEvent: "timeupdate",
        init: function(a, b) {
            this._super(a, b)
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-progress-holder"
            })
        },
        getPercent: function() {
            return this.player.currentTime() / this.player.duration()
        },
        onMouseDown: function(a) {
            this._super(a),
            this.player.scrubbing = !0,
            this.videoWasPlaying = !this.player.paused(),
            this.player.pause()
        },
        onMouseMove: function(a) {
            var b = this.calculateDistance(a) * this.player.duration();
            b == this.player.duration() && (b -= .1),
            this.player.currentTime(b)
        },
        onMouseUp: function(a) {
            this._super(a),
            this.player.scrubbing = !1,
            this.videoWasPlaying && this.player.play()
        },
        stepForward: function() {
            this.player.currentTime(this.player.currentTime() + 1)
        },
        stepBack: function() {
            this.player.currentTime(this.player.currentTime() - 1)
        }
    }),
    _V_.LoadProgressBar = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("progress", _V_.proxy(this, this.update))
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-load-progress",
                innerHTML: '<span class="vjs-control-text">Loaded: 0%</span>'
            })
        },
        update: function() {
            this.el.style && (this.el.style.width = _V_.round(this.player.bufferedPercent() * 100, 2) + "%")
        }
    }),
    _V_.PlayProgressBar = _V_.Component.extend({
        createElement: function() {
            return this._super("div", {
                className: "vjs-play-progress",
                innerHTML: '<span class="vjs-control-text">Progress: 0%</span>'
            })
        }
    }),
    _V_.SeekHandle = _V_.Component.extend({
        createElement: function() {
            return this._super("div", {
                className: "vjs-seek-handle",
                innerHTML: '<span class="vjs-control-text">00:00</span>'
            })
        }
    }),
    _V_.VolumeControl = _V_.Component.extend({
        options: {
            components: {
                volumeBar: {}
            }
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-volume-control vjs-control"
            })
        }
    }),
    _V_.VolumeBar = _V_.Slider.extend({
        options: {
            components: {
                bar: {
                    componentClass: "VolumeLevel"
                },
                handle: {
                    componentClass: "VolumeHandle"
                }
            }
        },
        playerEvent: "volumechange",
        createElement: function() {
            return this._super("div", {
                className: "vjs-volume-bar"
            })
        },
        onMouseMove: function(a) {
            this.player.volume(this.calculateDistance(a))
        },
        getPercent: function() {
            return this.player.volume()
        },
        stepForward: function() {
            this.player.volume(this.player.volume() + .1)
        },
        stepBack: function() {
            this.player.volume(this.player.volume() - .1)
        }
    }),
    _V_.VolumeLevel = _V_.Component.extend({
        createElement: function() {
            return this._super("div", {
                className: "vjs-volume-level",
                innerHTML: '<span class="vjs-control-text"></span>'
            })
        }
    }),
    _V_.VolumeHandle = _V_.Component.extend({
        createElement: function() {
            return this._super("div", {
                className: "vjs-volume-handle",
                innerHTML: '<span class="vjs-control-text"></span>'
            })
        }
    }),
    _V_.MuteToggle = _V_.Button.extend({
        init: function(a, b) {
            this._super(a, b),
            a.addEvent("volumechange", _V_.proxy(this, this.update))
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-mute-control vjs-control",
                innerHTML: '<div><span class="vjs-control-text">Mute</span></div>'
            })
        },
        onClick: function(a) {
            this.player.muted(this.player.muted() ? !1 : !0)
        },
        update: function(a) {
            var b = this.player.volume(),
            c = 3;
            b == 0 || this.player.muted() ? c = 0 : b < .33 ? c = 1 : b < .67 && (c = 2),
            _V_.each.call(this, [0, 1, 2, 3],
            function(a) {
                _V_.removeClass(this.el, "vjs-vol-" + a)
            }),
            _V_.addClass(this.el, "vjs-vol-" + c)
        }
    }),
    _V_.PosterImage = _V_.Button.extend({
        init: function(a, b) {
            this._super(a, b),
            this.player.options.poster || this.hide(),
            a.addEvent("play", _V_.proxy(this, this.hide))
        },
        createElement: function() {
            return _V_.createElement("img", {
                className: "vjs-poster",
                src: this.player.options.poster,
                tabIndex: -1
            })
        },
        onClick: function() {
            this.player.play()
        }
    }),
    _V_.Menu = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b)
        },
        addItem: function(a) {
            this.addComponent(a),
            a.addEvent("click", this.proxy(function() {
                this.unlockShowing()
            }))
        },
        createElement: function() {
            return this._super("ul", {
                className: "vjs-menu"
            })
        }
    }),
    _V_.MenuItem = _V_.Button.extend({
        init: function(a, b) {
            this._super(a, b),
            b.selected && this.addClass("vjs-selected")
        },
        createElement: function(a, b) {
            return this._super("li", _V_.merge({
                className: "vjs-menu-item",
                innerHTML: this.options.label
            },
            b))
        },
        onClick: function() {
            this.selected(!0)
        },
        selected: function(a) {
            a ? this.addClass("vjs-selected") : this.removeClass("vjs-selected")
        }
    }),
    Array.prototype.indexOf || (Array.prototype.indexOf = function(a) {
        "use strict";
        if (this === void 0 || this === null) throw new TypeError;
        var b = Object(this),
        c = b.length >>> 0;
        if (c === 0) return - 1;
        var d = 0;
        arguments.length > 0 && (d = Number(arguments[1]), d !== d ? d = 0 : d !== 0 && d !== 1 / 0 && d !== -Infinity && (d = (d > 0 || -1) * Math.floor(Math.abs(d))));
        if (d >= c) return - 1;
        var e = d >= 0 ? d: Math.max(c - Math.abs(d), 0);
        for (; e < c; e++) if (e in b && b[e] === a) return e;
        return - 1
    }),
    _V_.extend({
        addEvent: function(a, b, c) {
            var d = _V_.getData(a),
            e;
            d && !d.handler && (d.handler = function(b) {
                b = _V_.fixEvent(b);
                var c = _V_.getData(a).events[b.type];
                if (c) {
                    var d = [];
                    _V_.each(c,
                    function(a, b) {
                        d[b] = a
                    });
                    for (var e = 0, f = d.length; e < f; e++) d[e].call(a, b)
                }
            }),
            d.events || (d.events = {}),
            e = d.events[b],
            e || (e = d.events[b] = [], document.addEventListener ? a.addEventListener(b, d.handler, !1) : document.attachEvent && a.attachEvent("on" + b, d.handler)),
            c.guid || (c.guid = _V_.guid++),
            e.push(c)
        },
        removeEvent: function(a, b, c) {
            var d = _V_.getData(a),
            e;
            if (!d.events) return;
            if (!b) {
                for (b in d.events) _V_.cleanUpEvents(a, b);
                return
            }
            e = d.events[b];
            if (!e) return;
            if (c && c.guid) for (var f = 0; f < e.length; f++) e[f].guid === c.guid && e.splice(f--, 1);
            _V_.cleanUpEvents(a, b)
        },
        cleanUpEvents: function(a, b) {
            var c = _V_.getData(a);
            c.events[b].length === 0 && (delete c.events[b], document.removeEventListener ? a.removeEventListener(b, c.handler, !1) : document.detachEvent && a.detachEvent("on" + b, c.handler)),
            _V_.isEmpty(c.events) && (delete c.events, delete c.handler),
            _V_.isEmpty(c) && _V_.removeData(a)
        },
        fixEvent: function(a) {
            if (a[_V_.expando]) return a;
            var b = a;
            a = new _V_.Event(b);
            for (var c = _V_.Event.props.length, d; c;) d = _V_.Event.props[--c],
            a[d] = b[d];
            a.target || (a.target = a.srcElement || document),
            a.target.nodeType === 3 && (a.target = a.target.parentNode),
            !a.relatedTarget && a.fromElement && (a.relatedTarget = a.fromElement === a.target ? a.toElement: a.fromElement);
            if (a.pageX == null && a.clientX != null) {
                var e = a.target.ownerDocument || document,
                f = e.documentElement,
                g = e.body;
                a.pageX = a.clientX + (f && f.scrollLeft || g && g.scrollLeft || 0) - (f && f.clientLeft || g && g.clientLeft || 0),
                a.pageY = a.clientY + (f && f.scrollTop || g && g.scrollTop || 0) - (f && f.clientTop || g && g.clientTop || 0)
            }
            return a.which == null && (a.charCode != null || a.keyCode != null) && (a.which = a.charCode != null ? a.charCode: a.keyCode),
            !a.metaKey && a.ctrlKey && (a.metaKey = a.ctrlKey),
            !a.which && a.button !== undefined && (a.which = a.button & 1 ? 1 : a.button & 2 ? 3 : a.button & 4 ? 2 : 0),
            a
        },
        triggerEvent: function(a, b) {
            var c = _V_.getData(a),
            d = a.parentNode || a.ownerDocument,
            e = b.type || b,
            f;
            c && (f = c.handler),
            b = typeof b == "object" ? b[_V_.expando] ? b: new _V_.Event(e, b) : new _V_.Event(e),
            b.type = e,
            f && f.call(a, b),
            b.result = undefined,
            b.target = a
        },
        one: function(a, b, c) {
            _V_.addEvent(a, b,
            function() {
                _V_.removeEvent(a, b, arguments.callee),
                c.apply(this, arguments)
            })
        }
    }),
    _V_.Event = function(a, b) {
        a && a.type ? (this.originalEvent = a, this.type = a.type, this.isDefaultPrevented = a.defaultPrevented || a.returnValue === !1 || a.getPreventDefault && a.getPreventDefault() ? returnTrue: returnFalse) : this.type = a,
        b && _V_.merge(this, b),
        this.timeStamp = (new Date).getTime(),
        this[_V_.expando] = !0
    },
    _V_.Event.prototype = {
        preventDefault: function() {
            this.isDefaultPrevented = returnTrue;
            var a = this.originalEvent;
            if (!a) return;
            a.preventDefault ? a.preventDefault() : a.returnValue = !1
        },
        stopPropagation: function() {
            this.isPropagationStopped = returnTrue;
            var a = this.originalEvent;
            if (!a) return;
            a.stopPropagation && a.stopPropagation(),
            a.cancelBubble = !0
        },
        stopImmediatePropagation: function() {
            this.isImmediatePropagationStopped = returnTrue,
            this.stopPropagation()
        },
        isDefaultPrevented: returnFalse,
        isPropagationStopped: returnFalse,
        isImmediatePropagationStopped: returnFalse
    },
    _V_.Event.props = "altKey attrChange attrName bubbles button cancelable charCode clientX clientY ctrlKey currentTarget data detail eventPhase fromElement handler keyCode metaKey newValue offsetX offsetY pageX pageY prevValue relatedNode relatedTarget screenX screenY shiftKey srcElement target toElement view wheelDelta which".split(" ");
    var JSON;
    JSON || (JSON = {}),
    function() {
        var cx = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
        typeof JSON.parse != "function" && (JSON.parse = function(text, reviver) {
            function walk(a, b) {
                var c, d, e = a[b];
                if (e && typeof e == "object") for (c in e) Object.prototype.hasOwnProperty.call(e, c) && (d = walk(e, c), d !== undefined ? e[c] = d: delete e[c]);
                return reviver.call(a, b, e)
            }
            var j;
            text = String(text),
            cx.lastIndex = 0,
            cx.test(text) && (text = text.replace(cx,
            function(a) {
                return "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice( - 4)
            }));
            if (/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) return j = eval("(" + text + ")"),
            typeof reviver == "function" ? walk({
                "": j
            },
            "") : j;
            throw new SyntaxError("JSON.parse")
        })
    } (),
    _V_.Player = _V_.Component.extend({
        init: function(a, b, c) {
            this.tag = a;
            var d = this.el = _V_.createElement("div"),
            e = this.options = {},
            f = e.width = a.getAttribute("width"),
            g = e.height = a.getAttribute("height"),
            h = f || 300,
            i = g || 150;
            a.player = d.player = this,
            this.ready(c),
            a.parentNode.insertBefore(d, a),
            d.appendChild(a),
            d.id = this.id = a.id,
            d.className = a.className,
            a.id += "_html5_api",
            a.className = "vjs-tech",
            _V_.players[d.id] = this,
            d.setAttribute("width", h),
            d.setAttribute("height", i),
            d.style.width = h + "px",
            d.style.height = i + "px",
            a.removeAttribute("width"),
            a.removeAttribute("height"),
            _V_.merge(e, _V_.options),
            _V_.merge(e, this.getVideoTagSettings()),
            _V_.merge(e, b),
            a.removeAttribute("controls"),
            a.removeAttribute("poster");
            if (a.hasChildNodes()) for (var j = 0, k = a.childNodes; j < k.length; j++)(k[j].nodeName == "SOURCE" || k[j].nodeName == "TRACK") && a.removeChild(k[j]);
            this.values = {},
            this.addClass("vjs-paused"),
            this.addEvent("ended", this.onEnded),
            this.addEvent("play", this.onPlay),
            this.addEvent("pause", this.onPause),
            this.addEvent("progress", this.onProgress),
            this.addEvent("error", this.onError),
            e.controls && this.ready(function() {
                this.initComponents()
            }),
            this.textTracks = [],
            e.tracks && e.tracks.length > 0 && this.addTextTracks(e.tracks);
            if (!e.sources || e.sources.length == 0) for (var j = 0, k = e.techOrder; j < k.length; j++) {
                var l = k[j],
                m = _V_[l];
                if (m.isSupported()) {
                    this.loadTech(l);
                    break
                }
            } else this.src(e.sources)
        },
        values: {},
        destroy: function() {
            this.stopTrackingProgress(),
            this.stopTrackingCurrentTime(),
            _V_.players[this.id] = null,
            delete _V_.players[this.id],
            this.tech.destroy(),
            this.el.parentNode.removeChild(this.el)
        },
        createElement: function(a, b) {},
        getVideoTagSettings: function() {
            var a = {
                sources: [],
                tracks: []
            };
            a.src = this.tag.getAttribute("src"),
            a.controls = this.tag.getAttribute("controls") !== null,
            a.poster = this.tag.getAttribute("poster"),
            a.preload = this.tag.getAttribute("preload"),
            a.autoplay = this.tag.getAttribute("autoplay") !== null,
            a.loop = this.tag.getAttribute("loop") !== null,
            a.muted = this.tag.getAttribute("muted") !== null;
            if (this.tag.hasChildNodes()) for (var b, c = 0, d = this.tag.childNodes; c < d.length; c++) b = d[c],
            b.nodeName == "SOURCE" && a.sources.push({
                src: b.getAttribute("src"),
                type: b.getAttribute("type"),
                media: b.getAttribute("media"),
                title: b.getAttribute("title")
            }),
            b.nodeName == "TRACK" && a.tracks.push({
                src: b.getAttribute("src"),
                kind: b.getAttribute("kind"),
                srclang: b.getAttribute("srclang"),
                label: b.getAttribute("label"),
                "default": b.getAttribute("default") !== null,
                title: b.getAttribute("title")
            });
            return a
        },
        loadTech: function(a, b) {
            this.tech ? this.unloadTech() : a != "html5" && this.tag && (this.el.removeChild(this.tag), this.tag = !1),
            this.techName = a,
            this.isReady = !1;
            var c = function() {
                this.player.triggerReady(),
                this.support.progressEvent || this.player.manualProgressOn(),
                this.support.timeupdateEvent || this.player.manualTimeUpdatesOn()
            },
            d = _V_.merge({
                source: b,
                parentEl: this.el
            },
            this.options[a]);
            b && (b.src == this.values.src && this.values.currentTime > 0 && (d.startTime = this.values.currentTime), this.values.src = b.src),
            this.tech = new _V_[a](this, d),
            this.tech.ready(c)
        },
        unloadTech: function() {
            this.tech.destroy(),
            this.manualProgress && this.manualProgressOff(),
            this.manualTimeUpdates && this.manualTimeUpdatesOff(),
            this.tech = !1
        },
        manualProgressOn: function() {
            this.manualProgress = !0,
            this.trackProgress(),
            this.tech.addEvent("progress",
            function() {
                this.removeEvent("progress", arguments.callee),
                this.support.progressEvent = !0,
                this.player.manualProgressOff()
            })
        },
        manualProgressOff: function() {
            this.manualProgress = !1,
            this.stopTrackingProgress()
        },
        trackProgress: function() {
            this.progressInterval = setInterval(_V_.proxy(this,
            function() {
                this.values.bufferEnd < this.buffered().end(0) ? this.triggerEvent("progress") : this.bufferedPercent() == 1 && (this.stopTrackingProgress(), this.triggerEvent("progress"))
            }), 500)
        },
        stopTrackingProgress: function() {
            clearInterval(this.progressInterval)
        },
        manualTimeUpdatesOn: function() {
            this.manualTimeUpdates = !0,
            this.addEvent("play", this.trackCurrentTime),
            this.addEvent("pause", this.stopTrackingCurrentTime),
            this.tech.addEvent("timeupdate",
            function() {
                this.removeEvent("timeupdate", arguments.callee),
                this.support.timeupdateEvent = !0,
                this.player.manualTimeUpdatesOff()
            })
        },
        manualTimeUpdatesOff: function() {
            this.manualTimeUpdates = !1,
            this.stopTrackingCurrentTime(),
            this.removeEvent("play", this.trackCurrentTime),
            this.removeEvent("pause", this.stopTrackingCurrentTime)
        },
        trackCurrentTime: function() {
            this.currentTimeInterval && this.stopTrackingCurrentTime(),
            this.currentTimeInterval = setInterval(_V_.proxy(this,
            function() {
                this.triggerEvent("timeupdate")
            }), 250)
        },
        stopTrackingCurrentTime: function() {
            clearInterval(this.currentTimeInterval)
        },
        onEnded: function() {
            this.options.loop ? (this.currentTime(0), this.play()) : (this.pause(), this.currentTime(0), this.pause())
        },
        onPlay: function() {
            _V_.removeClass(this.el, "vjs-paused"),
            _V_.addClass(this.el, "vjs-playing")
        },
        onPause: function() {
            _V_.removeClass(this.el, "vjs-playing"),
            _V_.addClass(this.el, "vjs-paused")
        },
        onProgress: function() {
            this.bufferedPercent() == 1 && this.triggerEvent("loadedalldata")
        },
        onError: function(a) {
            _V_.log("Video Error", a)
        },
        techCall: function(a, b) {
            if (!this.tech.isReady) this.tech.ready(function() {
                this[a](b)
            });
            else try {
                this.tech[a](b)
            } catch(c) {
                _V_.log(c)
            }
        },
        techGet: function(a) {
            if (this.tech.isReady) try {
                return this.tech[a]()
            } catch(b) {
                this.tech[a] === undefined ? _V_.log("Video.js: " + a + " method not defined for " + this.techName + " playback technology.", b) : b.name == "TypeError" ? (_V_.log("Video.js: " + a + " unavailable on " + this.techName + " playback technology element.", b), this.tech.isReady = !1) : _V_.log(b)
            }
            return
        },
        play: function() {
            return this.techCall("play"),
            this
        },
        pause: function() {
            return this.techCall("pause"),
            this
        },
        paused: function() {
            return this.techGet("paused") === !1 ? !1 : !0
        },
        currentTime: function(a) {
            return a !== undefined ? (this.values.lastSetCurrentTime = a, this.techCall("setCurrentTime", a), this.manualTimeUpdates && this.triggerEvent("timeupdate"), this) : this.values.currentTime = this.techGet("currentTime") || 0
        },
        duration: function() {
            return parseFloat(this.techGet("duration"))
        },
        remainingTime: function() {
            return this.duration() - this.currentTime()
        },
        buffered: function() {
            var a = this.techGet("buffered"),
            b = 0,
            c = this.values.bufferEnd = this.values.bufferEnd || 0,
            d;
            return a && a.length > 0 && a.end(0) !== c && (c = a.end(0), this.values.bufferEnd = c),
            _V_.createTimeRange(b, c)
        },
        bufferedPercent: function() {
            return this.duration() ? this.buffered().end(0) / this.duration() : 0
        },
        volume: function(a) {
            var b;
            return a !== undefined ? (b = Math.max(0, Math.min(1, parseFloat(a))), this.values.volume = b, this.techCall("setVolume", b), _V_.setLocalStorage("volume", b), this) : (b = parseFloat(this.techGet("volume")), isNaN(b) ? 1 : b)
        },
        muted: function(a) {
            return a !== undefined ? (this.techCall("setMuted", a), this) : this.techGet("muted") || !1
        },
        width: function(a, b) {
            return a !== undefined ? (this.el.width = a, this.el.style.width = a + "px", b || this.triggerEvent("resize"), this) : parseInt(this.el.getAttribute("width"))
        },
        height: function(a) {
            return a !== undefined ? (this.el.height = a, this.el.style.height = a + "px", this.triggerEvent("resize"), this) : parseInt(this.el.getAttribute("height"))
        },
        size: function(a, b) {
            return this.width(a, !0).height(b)
        },
        supportsFullScreen: function() {
            return this.techGet("supportsFullScreen") || !1
        },
        requestFullScreen: function() {
            var a = _V_.support.requestFullScreen;
            return this.isFullScreen = !0,
            a ? (_V_.addEvent(document, a.eventName, this.proxy(function() {
                this.isFullScreen = document[a.isFullScreen],
                this.isFullScreen == 0 && _V_.removeEvent(document, a.eventName, arguments.callee),
                this.triggerEvent("fullscreenchange")
            })), this.tech.support.fullscreenResize === !1 && this.options.flash.iFrameMode != 1 ? (this.pause(), this.unloadTech(), _V_.addEvent(document, a.eventName, this.proxy(function() {
                _V_.removeEvent(document, a.eventName, arguments.callee),
                this.loadTech(this.techName, {
                    src: this.values.src
                })
            })), this.el[a.requestFn]()) : this.el[a.requestFn]()) : this.tech.supportsFullScreen() ? (this.triggerEvent("fullscreenchange"), this.techCall("enterFullScreen")) : (this.triggerEvent("fullscreenchange"), this.enterFullWindow()),
            this
        },
        cancelFullScreen: function() {
            var a = _V_.support.requestFullScreen;
            return this.isFullScreen = !1,
            a ? this.tech.support.fullscreenResize === !1 && this.options.flash.iFrameMode != 1 ? (this.pause(), this.unloadTech(), _V_.addEvent(document, a.eventName, this.proxy(function() {
                _V_.removeEvent(document, a.eventName, arguments.callee),
                this.loadTech(this.techName, {
                    src: this.values.src
                })
            })), document[a.cancelFn]()) : document[a.cancelFn]() : this.tech.supportsFullScreen() ? (this.techCall("exitFullScreen"), this.triggerEvent("fullscreenchange")) : (this.exitFullWindow(), this.triggerEvent("fullscreenchange")),
            this
        },
        enterFullWindow: function() {
            this.isFullWindow = !0,
            this.docOrigOverflow = document.documentElement.style.overflow,
            _V_.addEvent(document, "keydown", _V_.proxy(this, this.fullWindowOnEscKey)),
            document.documentElement.style.overflow = "hidden",
            _V_.addClass(document.body, "vjs-full-window"),
            _V_.addClass(this.el, "vjs-fullscreen"),
            this.triggerEvent("enterFullWindow")
        },
        fullWindowOnEscKey: function(a) {
            a.keyCode == 27 && (this.isFullScreen == 1 ? this.cancelFullScreen() : this.exitFullWindow())
        },
        exitFullWindow: function() {
            this.isFullWindow = !1,
            _V_.removeEvent(document, "keydown", this.fullWindowOnEscKey),
            document.documentElement.style.overflow = this.docOrigOverflow,
            _V_.removeClass(document.body, "vjs-full-window"),
            _V_.removeClass(this.el, "vjs-fullscreen"),
            this.triggerEvent("exitFullWindow")
        },
        selectSource: function(a) {
            for (var b = 0, c = this.options.techOrder; b < c.length; b++) {
                var d = c[b],
                e = _V_[d];
                if (e.isSupported()) for (var f = 0, g = a; f < g.length; f++) {
                    var h = g[f];
                    if (e.canPlaySource.call(this, h)) return {
                        source: h,
                        tech: d
                    }
                }
            }
            return ! 1
        },
        src: function(a) {
            if (a instanceof Array) {
                var b = this.selectSource(a),
                a,
                c;
                b ? (a = b.source, c = b.tech, c == this.techName ? this.src(a) : this.loadTech(c, a)) : _V_.log("No compatible source and playback technology were found.")
            } else a instanceof Object ? _V_[this.techName].canPlaySource(a) ? this.src(a.src) : this.src([a]) : (this.values.src = a, this.isReady ? (this.techCall("src", a), this.options.preload == "auto" && this.load(), this.options.autoplay && this.play()) : this.ready(function() {
                this.src(a)
            }));
            return this
        },
        load: function() {
            return this.techCall("load"),
            this
        },
        currentSrc: function() {
            return this.techGet("currentSrc") || this.values.src || ""
        },
        preload: function(a) {
            return a !== undefined ? (this.techCall("setPreload", a), this.options.preload = a, this) : this.techGet("preload")
        },
        autoplay: function(a) {
            return a !== undefined ? (this.techCall("setAutoplay", a), this.options.autoplay = a, this) : this.techGet("autoplay", a)
        },
        loop: function(a) {
            return a !== undefined ? (this.techCall("setLoop", a), this.options.loop = a, this) : this.techGet("loop")
        },
        controls: function() {
            return this.options.controls
        },
        poster: function() {
            return this.techGet("poster")
        },
        error: function() {
            return this.techGet("error")
        },
        ended: function() {
            return this.techGet("ended")
        }
    }),
    function() {
        var a, b, c, d, e = _V_.Player.prototype;
        document.cancelFullscreen !== undefined ? (a = "requestFullscreen", b = "exitFullscreen", c = "fullscreenchange", d = "fullScreen") : _V_.each(["moz", "webkit"],
        function(e) { (e != "moz" || document.mozFullScreenEnabled) && document[e + "CancelFullScreen"] !== undefined && (a = e + "RequestFullScreen", b = e + "CancelFullScreen", c = e + "fullscreenchange", e == "webkit" ? d = e + "IsFullScreen": d = e + "FullScreen")
        }),
        a && (_V_.support.requestFullScreen = {
            requestFn: a,
            cancelFn: b,
            eventName: c,
            isFullScreen: d
        })
    } (),
    _V_.PlaybackTech = _V_.Component.extend({
        init: function(a, b) {},
        onClick: function() {
            this.player.options.controls && _V_.PlayToggle.prototype.onClick.call(this)
        }
    }),
    _V_.apiMethods = "play,pause,paused,currentTime,setCurrentTime,duration,buffered,volume,setVolume,muted,setMuted,width,height,supportsFullScreen,enterFullScreen,src,load,currentSrc,preload,setPreload,autoplay,setAutoplay,loop,setLoop,error,networkState,readyState,seeking,initialTime,startOffsetTime,played,seekable,ended,videoTracks,audioTracks,videoWidth,videoHeight,textTracks,defaultPlaybackRate,playbackRate,mediaGroup,controller,controls,defaultMuted".split(","),
    _V_.each(_V_.apiMethods,
    function(a) {
        _V_.PlaybackTech.prototype[a] = function() {
            throw new Error("The '" + a + "' method is not available on the playback technology's API")
        }
    }),
    _V_.html5 = _V_.PlaybackTech.extend({
        init: function(a, b, c) {
            this.player = a,
            this.el = this.createElement(),
            this.ready(c),
            this.addEvent("click", this.proxy(this.onClick));
            var d = b.source;
            d && this.el.currentSrc == d.src ? a.triggerEvent("loadstart") : d && (this.el.src = d.src),
            a.ready(function() {
                this.options.autoplay && this.paused() && (this.tag.poster = null, this.play())
            }),
            this.setupTriggers(),
            this.triggerReady()
        },
        destroy: function() {
            this.player.tag = !1,
            this.removeTriggers(),
            this.el.parentNode.removeChild(this.el)
        },
        createElement: function() {
            var a = _V_.html5,
            b = this.player,
            c = b.tag,
            d;
            if (!c || this.support.movingElementInDOM === !1) c && b.el.removeChild(c),
            d = _V_.createElement("video", {
                id: c.id || b.el.id + "_html5_api",
                className: c.className || "vjs-tech"
            }),
            c = d,
            _V_.insertFirst(c, b.el);
            return _V_.each(["autoplay", "preload", "loop", "muted"],
            function(a) {
                b.options[a] !== null && (c[a] = b.options[a])
            },
            this),
            c
        },
        setupTriggers: function() {
            _V_.each.call(this, _V_.html5.events,
            function(a) {
                _V_.addEvent(this.el, a, _V_.proxy(this.player, this.eventHandler))
            })
        },
        removeTriggers: function() {
            _V_.each.call(this, _V_.html5.events,
            function(a) {
                _V_.removeEvent(this.el, a, _V_.proxy(this.player, this.eventHandler))
            })
        },
        eventHandler: function(a) {
            a.stopPropagation(),
            this.triggerEvent(a)
        },
        play: function() {
            this.el.play()
        },
        pause: function() {
            this.el.pause()
        },
        paused: function() {
            return this.el.paused
        },
        currentTime: function() {
            return this.el.currentTime
        },
        setCurrentTime: function(a) {
            try {
                this.el.currentTime = a
            } catch(b) {
                _V_.log(b, "Video isn't ready. (VideoJS)")
            }
        },
        duration: function() {
            return this.el.duration || 0
        },
        buffered: function() {
            return this.el.buffered
        },
        volume: function() {
            return this.el.volume
        },
        setVolume: function(a) {
            this.el.volume = a
        },
        muted: function() {
            return this.el.muted
        },
        setMuted: function(a) {
            this.el.muted = a
        },
        width: function() {
            return this.el.offsetWidth
        },
        height: function() {
            return this.el.offsetHeight
        },
        supportsFullScreen: function() {
            return typeof this.el.webkitEnterFullScreen == "function" && !navigator.userAgent.match("Chrome") && !navigator.userAgent.match("Mac OS X 10.5") ? !0 : !1
        },
        enterFullScreen: function() {
            try {
                this.el.webkitEnterFullScreen()
            } catch(a) {
                a.code == 11 && _V_.log("VideoJS: Video not ready.")
            }
        },
        src: function(a) {
            this.el.src = a
        },
        load: function() {
            this.el.load()
        },
        currentSrc: function() {
            return this.el.currentSrc
        },
        preload: function() {
            return this.el.preload
        },
        setPreload: function(a) {
            this.el.preload = a
        },
        autoplay: function() {
            return this.el.autoplay
        },
        setAutoplay: function(a) {
            this.el.autoplay = a
        },
        loop: function() {
            return this.el.loop
        },
        setLoop: function(a) {
            this.el.loop = a
        },
        error: function() {
            return this.el.error
        },
        seeking: function() {
            return this.el.seeking
        },
        ended: function() {
            return this.el.ended
        },
        controls: function() {
            return this.player.options.controls
        },
        defaultMuted: function() {
            return this.el.defaultMuted
        }
    }),
    _V_.html5.isSupported = function() {
        return !! document.createElement("video").canPlayType
    },
    _V_.html5.canPlaySource = function(a) {
        return !! document.createElement("video").canPlayType(a.type)
    },
    _V_.html5.events = "loadstart,suspend,abort,error,emptied,stalled,loadedmetadata,loadeddata,canplay,canplaythrough,playing,waiting,seeking,seeked,ended,durationchange,timeupdate,progress,play,pause,ratechange,volumechange".split(","),
    _V_.html5.prototype.support = {
        fullscreen: typeof _V_.testVid.webkitEnterFullScreen !== undefined ? !_V_.ua.match("Chrome") && !_V_.ua.match("Mac OS X 10.5") ? !0 : !1 : !1,
        movingElementInDOM: !_V_.isIOS()
    },
    _V_.isAndroid() && _V_.androidVersion() < 3 && (document.createElement("video").constructor.prototype.canPlayType = function(a) {
        return a && a.toLowerCase().indexOf("video/mp4") != -1 ? "maybe": ""
    }),
    _V_.flash = _V_.PlaybackTech.extend({
        init: function(a, b) {
            this.player = a;
            var c = b.source,
            d = b.parentEl,
            e = this.el = _V_.createElement("div", {
                id: d.id + "_temp_flash"
            }),
            f = a.el.id + "_flash_api",
            g = a.options,
            h = _V_.merge({
                readyFunction: "_V_.flash.onReady",
                eventProxyFunction: "_V_.flash.onEvent",
                errorEventProxyFunction: "_V_.flash.onError",
                autoplay: g.autoplay,
                preload: g.preload,
                loop: g.loop,
                muted: g.muted
            },
            b.flashVars),
            i = _V_.merge({
                wmode: "opaque",
                bgcolor: "#000000"
            },
            b.params),
            j = _V_.merge({
                id: f,
                name: f,
                "class": "vjs-tech"
            },
            b.attributes);
            c && (h.src = encodeURIComponent(_V_.getAbsoluteURL(c.src))),
            _V_.insertFirst(e, d),
            b.startTime && this.ready(function() {
                this.load(),
                this.play(),
                this.currentTime(b.startTime)
            });
            if (b.iFrameMode == 1 && !_V_.isFF) {
                var k = _V_.createElement("iframe", {
                    id: f + "_iframe",
                    name: f + "_iframe",
                    className: "vjs-tech",
                    scrolling: "no",
                    marginWidth: 0,
                    marginHeight: 0,
                    frameBorder: 0
                });
                h.readyFunction = "ready",
                h.eventProxyFunction = "events",
                h.errorEventProxyFunction = "errors",
                _V_.addEvent(k, "load", _V_.proxy(this,
                function() {
                    var a, c, d, e = k.contentWindow,
                    f = "";
                    a = k.contentDocument ? k.contentDocument: k.contentWindow.document,
                    a.write(_V_.flash.getEmbedCode(b.swf, h, i, j)),
                    e.player = this.player,
                    e.ready = _V_.proxy(this.player,
                    function(b) {
                        var c = a.getElementById(b),
                        d = this,
                        e = d.tech;
                        e.el = c,
                        _V_.addEvent(c, "click", e.proxy(e.onClick)),
                        _V_.flash.checkReady(e)
                    }),
                    e.events = _V_.proxy(this.player,
                    function(a, b, c) {
                        var d = this;
                        d && d.techName == "flash" && d.triggerEvent(b)
                    }),
                    e.errors = _V_.proxy(this.player,
                    function(a, b) {
                        _V_.log("Flash Error", b)
                    })
                })),
                e.parentNode.replaceChild(k, e)
            } else _V_.flash.embed(b.swf, e, h, i, j)
        },
        destroy: function() {
            this.el.parentNode.removeChild(this.el)
        },
        play: function() {
            this.el.vjs_play()
        },
        pause: function() {
            this.el.vjs_pause()
        },
        src: function(a) {
            a = _V_.getAbsoluteURL(a),
            this.el.vjs_src(a);
            if (this.player.autoplay()) {
                var b = this;
                setTimeout(function() {
                    b.play()
                },
                0)
            }
        },
        load: function() {
            this.el.vjs_load()
        },
        poster: function() {
            this.el.vjs_getProperty("poster")
        },
        buffered: function() {
            return _V_.createTimeRange(0, this.el.vjs_getProperty("buffered"))
        },
        supportsFullScreen: function() {
            return ! 1
        },
        enterFullScreen: function() {
            return ! 1
        }
    }),
    function() {
        var a = _V_.flash.prototype,
        b = "preload,currentTime,defaultPlaybackRate,playbackRate,autoplay,loop,mediaGroup,controller,controls,volume,muted,defaultMuted".split(","),
        c = "error,currentSrc,networkState,readyState,seeking,initialTime,duration,startOffsetTime,paused,played,seekable,ended,videoTracks,audioTracks,videoWidth,videoHeight,textTracks".split(","),
        d = "load,play,pause".split(",");
        createSetter = function(b) {
            var c = b.charAt(0).toUpperCase() + b.slice(1);
            a["set" + c] = function(a) {
                return this.el.vjs_setProperty(b, a)
            }
        },
        createGetter = function(b) {
            a[b] = function() {
                return this.el.vjs_getProperty(b)
            }
        },
        _V_.each(b,
        function(a) {
            createGetter(a),
            createSetter(a)
        }),
        _V_.each(c,
        function(a) {
            createGetter(a)
        })
    } (),
    _V_.flash.isSupported = function() {
        return _V_.flash.version()[0] >= 10
    },
    _V_.flash.canPlaySource = function(a) {
        if (a.type in _V_.flash.prototype.support.formats) return "maybe"
    },
    _V_.flash.prototype.support = {
        formats: {
            "video/flv": "FLV",
            "video/x-flv": "FLV",
            "video/mp4": "MP4",
            "video/m4v": "MP4"
        },
        progressEvent: !1,
        timeupdateEvent: !1,
        fullscreenResize: !1,
        parentResize: !_V_.ua.match("Firefox")
    },
    _V_.flash.onReady = function(a) {
        var b = _V_.el(a),
        c = b.player || b.parentNode.player,
        d = c.tech;
        b.player = c,
        d.el = b,
        d.addEvent("click", d.onClick),
        _V_.flash.checkReady(d)
    },
    _V_.flash.checkReady = function(a) {
        a.el.vjs_getProperty ? a.triggerReady() : setTimeout(function() {
            _V_.flash.checkReady(a)
        },
        50)
    },
    _V_.flash.onEvent = function(a, b) {
        var c = _V_.el(a).player;
        c.triggerEvent(b)
    },
    _V_.flash.onError = function(a, b) {
        var c = _V_.el(a).player;
        c.triggerEvent("error"),
        _V_.log("Flash Error", b, a)
    },
    _V_.flash.version = function() {
        var a = "0,0,0";
        try {
            a = (new ActiveXObject("ShockwaveFlash.ShockwaveFlash")).GetVariable("$version").replace(/\D+/g, ",").match(/^,?(.+),?$/)[1]
        } catch(b) {
            try {
                navigator.mimeTypes["application/x-shockwave-flash"].enabledPlugin && (a = (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]).description.replace(/\D+/g, ",").match(/^,?(.+),?$/)[1])
            } catch(b) {}
        }
        return a.split(",")
    },
    _V_.flash.embed = function(a, b, c, d, e) {
        var f = _V_.flash.getEmbedCode(a, c, d, e),
        g = _V_.createElement("div", {
            innerHTML: f
        }).childNodes[0],
        h = b.parentNode;
        b.parentNode.replaceChild(g, b);
        if (_V_.isIE()) {
            var i = h.childNodes[0];
            setTimeout(function() {
                i.style.display = "block"
            },
            1e3)
        }
        return g
    },
    _V_.flash.getEmbedCode = function(a, b, c, d) {
        var e = '<object type="application/x-shockwave-flash"',
        f = "",
        g = "";
        return attrsString = "",
        b && _V_.eachProp(b,
        function(a, b) {
            f += a + "=" + b + "&amp;"
        }),
        c = _V_.merge({
            movie: a,
            flashvars: f,
            allowScriptAccess: "always",
            allowNetworking: "all"
        },
        c),
        _V_.eachProp(c,
        function(a, b) {
            g += '<param name="' + a + '" value="' + b + '" />'
        }),
        d = _V_.merge({
            data: a,
            width: "100%",
            height: "100%"
        },
        d),
        _V_.eachProp(d,
        function(a, b) {
            attrsString += a + '="' + b + '" '
        }),
        e + attrsString + ">" + g + "</object>"
    },
    _V_.merge(_V_.Player.prototype, {
        addTextTracks: function(a) {
            var b = this.textTracks = this.textTracks ? this.textTracks: [],
            c = 0,
            d = a.length,
            e,
            f;
            for (; c < d; c++) f = _V_.uc(a[c].kind || "subtitles"),
            e = new _V_[f + "Track"](this, a[c]),
            b.push(e),
            e["default"] && this.ready(_V_.proxy(e, e.show));
            return this
        },
        showTextTrack: function(a, b) {
            var c = this.textTracks,
            d = 0,
            e = c.length,
            f, g, h;
            for (; d < e; d++) f = c[d],
            f.id === a ? (f.show(), g = f) : b && f.kind == b && f.mode > 0 && f.disable();
            return h = g ? g.kind: b ? b: !1,
            h && this.triggerEvent(h + "trackchange"),
            this
        }
    }),
    _V_.Track = _V_.Component.extend({
        init: function(a, b) {
            this._super(a, b),
            _V_.merge(this, {
                id: b.id || "vjs_" + b.kind + "_" + b.language + "_" + _V_.guid++,
                src: b.src,
                "default": b["default"],
                title: b.title,
                language: b.srclang,
                label: b.label,
                cues: [],
                activeCues: [],
                readyState: 0,
                mode: 0
            })
        },
        createElement: function() {
            return this._super("div", {
                className: "vjs-" + this.kind + " vjs-text-track"
            })
        },
        show: function() {
            this.activate(),
            this.mode = 2,
            this._super()
        },
        hide: function() {
            this.activate(),
            this.mode = 1,
            this._super()
        },
        disable: function() {
            this.mode == 2 && this.hide(),
            this.deactivate(),
            this.mode = 0
        },
        activate: function() {
            this.readyState == 0 && this.load(),
            this.mode == 0 && (this.player.addEvent("timeupdate", this.proxy(this.update, this.id)), this.player.addEvent("ended", this.proxy(this.reset, this.id)), (this.kind == "captions" || this.kind == "subtitles") && this.player.textTrackDisplay.addComponent(this))
        },
        deactivate: function() {
            this.player.removeEvent("timeupdate", this.proxy(this.update, this.id)),
            this.player.removeEvent("ended", this.proxy(this.reset, this.id)),
            this.reset(),
            this.player.textTrackDisplay.removeComponent(this)
        },
        load: function() {
            this.readyState == 0 && (this.readyState = 1, _V_.get(this.src, this.proxy(this.parseCues), this.proxy(this.onError)))
        },
        onError: function(a) {
            this.error = a,
            this.readyState = 3,
            this.triggerEvent("error")
        },
        parseCues: function(a) {
            var b, c, d, e = a.split("\n"),
            f = "",
            g;
            for (var h = 1, i = e.length; h < i; h++) {
                f = _V_.trim(e[h]);
                if (f) {
                    f.indexOf("-->") == -1 ? (g = f, f = _V_.trim(e[++h])) : g = this.cues.length,
                    b = {
                        id: g,
                        index: this.cues.length
                    },
                    c = f.split(" --> "),
                    b.startTime = this.parseCueTime(c[0]),
                    b.endTime = this.parseCueTime(c[1]),
                    d = [];
                    while (e[++h] && (f = _V_.trim(e[h]))) d.push(f);
                    b.text = d.join("<br/>"),
                    this.cues.push(b)
                }
            }
            this.readyState = 2,
            this.triggerEvent("loaded")
        },
        parseCueTime: function(a) {
            var b = a.split(":"),
            c = 0,
            d,
            e,
            f,
            g,
            h,
            i;
            return b.length == 3 ? (d = b[0], e = b[1], f = b[2]) : (d = 0, e = b[0], f = b[1]),
            f = f.split(/\s+/),
            g = f.splice(0, 1)[0],
            g = g.split(/\.|,/),
            h = parseFloat(g[1]),
            g = g[0],
            c += parseFloat(d) * 3600,
            c += parseFloat(e) * 60,
            c += parseFloat(g),
            h && (c += h / 1e3),
            c
        },
        update: function() {
            if (this.cues.length > 0) {
                var a = this.player.currentTime();
                if (this.prevChange === undefined || a < this.prevChange || this.nextChange <= a) {
                    var b = this.cues,
                    c = this.player.duration(),
                    d = 0,
                    e = !1,
                    f = [],
                    g,
                    h,
                    i = "",
                    j,
                    k,
                    l;
                    a >= this.nextChange || this.nextChange === undefined ? k = this.firstActiveIndex !== undefined ? this.firstActiveIndex: 0 : (e = !0, k = this.lastActiveIndex !== undefined ? this.lastActiveIndex: b.length - 1);
                    for (;;) {
                        j = b[k];
                        if (j.endTime <= a) d = Math.max(d, j.endTime),
                        j.active && (j.active = !1);
                        else if (a < j.startTime) {
                            c = Math.min(c, j.startTime),
                            j.active && (j.active = !1);
                            if (!e) break
                        } else e ? (f.splice(0, 0, j), h === undefined && (h = k), g = k) : (f.push(j), g === undefined && (g = k), h = k),
                        c = Math.min(c, j.endTime),
                        d = Math.max(d, j.startTime),
                        j.active = !0;
                        if (e) {
                            if (k === 0) break;
                            k--
                        } else {
                            if (k === b.length - 1) break;
                            k++
                        }
                    }
                    this.activeCues = f,
                    this.nextChange = c,
                    this.prevChange = d,
                    this.firstActiveIndex = g,
                    this.lastActiveIndex = h,
                    this.updateDisplay(),
                    this.triggerEvent("cuechange")
                }
            }
        },
        updateDisplay: function() {
            var a = this.activeCues,
            b = "",
            c = 0,
            d = a.length;
            for (; c < d; c++) b += "<span class='vjs-tt-cue'>" + a[c].text + "</span>";
            this.el.innerHTML = b
        },
        reset: function() {
            this.nextChange = 0,
            this.prevChange = this.player.duration(),
            this.firstActiveIndex = 0,
            this.lastActiveIndex = 0
        }
    }),
    _V_.CaptionsTrack = _V_.Track.extend({
        kind: "captions"
    }),
    _V_.SubtitlesTrack = _V_.Track.extend({
        kind: "subtitles"
    }),
    _V_.ChaptersTrack = _V_.Track.extend({
        kind: "chapters"
    }),
    _V_.TextTrackDisplay = _V_.Component.extend({
        createElement: function() {
            return this._super("div", {
                className: "vjs-text-track-display"
            })
        }
    }),
    _V_.TextTrackMenuItem = _V_.MenuItem.extend({
        init: function(a, b) {
            var c = this.track = b.track;
            b.label = c.label,
            b.selected = c["default"],
            this._super(a, b),
            this.player.addEvent(c.kind + "trackchange", _V_.proxy(this, this.update))
        },
        onClick: function() {
            this._super(),
            this.player.showTextTrack(this.track.id, this.track.kind)
        },
        update: function() {
            this.track.mode == 2 ? this.selected(!0) : this.selected(!1)
        }
    }),
    _V_.OffTextTrackMenuItem = _V_.TextTrackMenuItem.extend({
        init: function(a, b) {
            b.track = {
                kind: b.kind,
                player: a,
                label: "Off"
            },
            this._super(a, b)
        },
        onClick: function() {
            this._super(),
            this.player.showTextTrack(this.track.id, this.track.kind)
        },
        update: function() {
            var a = this.player.textTracks,
            b = 0,
            c = a.length,
            d, e = !0;
            for (; b < c; b++) d = a[b],
            d.kind == this.track.kind && d.mode == 2 && (e = !1);
            e ? this.selected(!0) : this.selected(!1)
        }
    }),
    _V_.TextTrackButton = _V_.Button.extend({
        init: function(a, b) {
            this._super(a, b),
            this.menu = this.createMenu(),
            this.items.length === 0 && this.hide()
        },
        createMenu: function() {
            var a = new _V_.Menu(this.player);
            return a.el.appendChild(_V_.createElement("li", {
                className: "vjs-menu-title",
                innerHTML: _V_.uc(this.kind)
            })),
            a.addItem(new _V_.OffTextTrackMenuItem(this.player, {
                kind: this.kind
            })),
            this.items = this.createItems(),
            this.each(this.items,
            function(b) {
                a.addItem(b)
            }),
            this.addComponent(a),
            a
        },
        createItems: function() {
            var a = [];
            return this.each(this.player.textTracks,
            function(b) {
                b.kind === this.kind && a.push(new _V_.TextTrackMenuItem(this.player, {
                    track: b
                }))
            }),
            a
        },
        buildCSSClass: function() {
            return this.className + " vjs-menu-button " + this._super()
        },
        onFocus: function() {
            this.menu.lockShowing(),
            _V_.one(this.menu.el.childNodes[this.menu.el.childNodes.length - 1], "blur", this.proxy(function() {
                this.menu.unlockShowing()
            }))
        },
        onBlur: function() {},
        onClick: function() {
            this.one("mouseout", this.proxy(function() {
                this.menu.unlockShowing(),
                this.el.blur()
            }))
        }
    }),
    _V_.CaptionsButton = _V_.TextTrackButton.extend({
        kind: "captions",
        buttonText: "Captions",
        className: "vjs-captions-button"
    }),
    _V_.SubtitlesButton = _V_.TextTrackButton.extend({
        kind: "subtitles",
        buttonText: "Subtitles",
        className: "vjs-subtitles-button"
    }),
    _V_.ChaptersButton = _V_.TextTrackButton.extend({
        kind: "chapters",
        buttonText: "Chapters",
        className: "vjs-chapters-button",
        createItems: function(a) {
            var b = [];
            return this.each(this.player.textTracks,
            function(a) {
                a.kind === this.kind && b.push(new _V_.TextTrackMenuItem(this.player, {
                    track: a
                }))
            }),
            b
        },
        createMenu: function() {
            var a = this.player.textTracks,
            b = 0,
            c = a.length,
            d, e, f = this.items = [];
            for (; b < c; b++) {
                d = a[b];
                if (d.kind == this.kind && d["default"]) {
                    if (d.readyState < 2) {
                        this.chaptersTrack = d,
                        d.addEvent("loaded", this.proxy(this.createMenu));
                        return
                    }
                    e = d;
                    break
                }
            }
            var g = this.menu = new _V_.Menu(this.player);
            g.el.appendChild(_V_.createElement("li", {
                className: "vjs-menu-title",
                innerHTML: _V_.uc(this.kind)
            }));
            if (e) {
                var h = e.cues,
                b = 0,
                c = h.length,
                i, j;
                for (; b < c; b++) i = h[b],
                j = new _V_.ChaptersTrackMenuItem(this.player, {
                    track: e,
                    cue: i
                }),
                f.push(j),
                g.addComponent(j)
            }
            return this.addComponent(g),
            this.items.length > 0 && this.show(),
            g
        }
    }),
    _V_.ChaptersTrackMenuItem = _V_.MenuItem.extend({
        init: function(a, b) {
            var c = this.track = b.track,
            d = this.cue = b.cue,
            e = a.currentTime();
            b.label = d.text,
            b.selected = d.startTime <= e && e < d.endTime,
            this._super(a, b),
            c.addEvent("cuechange", _V_.proxy(this, this.update))
        },
        onClick: function() {
            this._super(),
            this.player.currentTime(this.cue.startTime),
            this.update(this.cue.startTime)
        },
        update: function(a) {
            var b = this.cue,
            c = this.player.currentTime();
            b.startTime <= c && c < b.endTime ? this.selected(!0) : this.selected(!1)
        }
    }),
    _V_.merge(_V_.ControlBar.prototype.options.components, {
        subtitlesButton: {},
        captionsButton: {},
        chaptersButton: {}
    }),
    _V_.autoSetup = function() {
        var a, b, c, d = document.getElementsByTagName("video");
        if (d && d.length > 0) for (var e = 0, f = d.length; e < f; e++) {
            b = d[e];
            if (b && b.getAttribute) b.player === undefined && (a = b.getAttribute("data-setup"), a !== null && (a = JSON.parse(a || "{}"), c = _V_(b, a)));
            else {
                _V_.autoSetupTimeout(1);
                break
            }
        } else _V_.windowLoaded || _V_.autoSetupTimeout(1)
    },
    _V_.autoSetupTimeout = function(a) {
        setTimeout(_V_.autoSetup, a)
    },
    _V_.addEvent(window, "load",
    function() {
        _V_.windowLoaded = !0
    }),
    _V_.autoSetup(),
    window.VideoJS = window._V_ = VideoJS
} (window),
function(a) {
    function E(a, b) {
        return function(c) {
            return L(a.call(this, c), b)
        }
    }
    function F(a) {
        return function(b) {
            return this.lang().ordinal(a.call(this, b))
        }
    }
    function G() {}
    function H(a) {
        J(this, a)
    }
    function I(a) {
        var b = this._data = {},
        c = a.years || a.year || a.y || 0,
        d = a.months || a.month || a.M || 0,
        e = a.weeks || a.week || a.w || 0,
        f = a.days || a.day || a.d || 0,
        g = a.hours || a.hour || a.h || 0,
        h = a.minutes || a.minute || a.m || 0,
        i = a.seconds || a.second || a.s || 0,
        j = a.milliseconds || a.millisecond || a.ms || 0;
        this._milliseconds = j + i * 1e3 + h * 6e4 + g * 36e5,
        this._days = f + e * 7,
        this._months = d + c * 12,
        b.milliseconds = j % 1e3,
        i += K(j / 1e3),
        b.seconds = i % 60,
        h += K(i / 60),
        b.minutes = h % 60,
        g += K(h / 60),
        b.hours = g % 24,
        f += K(g / 24),
        f += e * 7,
        b.days = f % 30,
        d += K(f / 30),
        b.months = d % 12,
        c += K(d / 12),
        b.years = c
    }
    function J(a, b) {
        for (var c in b) b.hasOwnProperty(c) && (a[c] = b[c]);
        return a
    }
    function K(a) {
        return a < 0 ? Math.ceil(a) : Math.floor(a)
    }
    function L(a, b) {
        var c = a + "";
        while (c.length < b) c = "0" + c;
        return c
    }
    function M(a, b, c) {
        var d = b._milliseconds,
        e = b._days,
        f = b._months,
        g;
        d && a._d.setTime( + a + d * c),
        e && a.date(a.date() + e * c),
        f && (g = a.date(), a.date(1).month(a.month() + f * c).date(Math.min(g, a.daysInMonth())))
    }
    function N(a) {
        return Object.prototype.toString.call(a) === "[object Array]"
    }
    function O(a, b) {
        var c = Math.min(a.length, b.length),
        d = Math.abs(a.length - b.length),
        e = 0,
        f;
        for (f = 0; f < c; f++)~~a[f] !== ~~b[f] && e++;
        return e + d
    }
    function P(a, b) {
        return b.abbr = a,
        f[a] || (f[a] = new G),
        f[a].set(b),
        f[a]
    }
    function Q(a) {
        return a ? (!f[a] && g && require("./lang/" + a), f[a]) : b.fn._lang
    }
    function R(a) {
        return a.match(/\[.*\]/) ? a.replace(/^\[|\]$/g, "") : a.replace(/\\/g, "")
    }
    function S(a) {
        var b = a.match(i),
        c,
        d;
        for (c = 0, d = b.length; c < d; c++) D[b[c]] ? b[c] = D[b[c]] : b[c] = R(b[c]);
        return function(e) {
            var f = "";
            for (c = 0; c < d; c++) f += typeof b[c].call == "function" ? b[c].call(e, a) : b[c];
            return f
        }
    }
    function T(a, b) {
        function d(b) {
            return a.lang().longDateFormat(b) || b
        }
        var c = 5;
        while (c--&&j.test(b)) b = b.replace(j, d);
        return A[b] || (A[b] = S(b)),
        A[b](a)
    }
    function U(a) {
        switch (a) {
        case "DDDD":
            return n;
        case "YYYY":
            return o;
        case "YYYYY":
            return p;
        case "S":
        case "SS":
        case "SSS":
        case "DDD":
            return m;
        case "MMM":
        case "MMMM":
        case "dd":
        case "ddd":
        case "dddd":
        case "a":
        case "A":
            return q;
        case "X":
            return t;
        case "Z":
        case "ZZ":
            return r;
        case "T":
            return s;
        case "MM":
        case "DD":
        case "YY":
        case "HH":
        case "hh":
        case "mm":
        case "ss":
        case "M":
        case "D":
        case "d":
        case "H":
        case "h":
        case "m":
        case "s":
            return l;
        default:
            return new RegExp(a.replace("\\", ""))
        }
    }
    function V(a, b, c) {
        var d, e, f = c._a;
        switch (a) {
        case "M":
        case "MM":
            f[1] = b == null ? 0 : ~~b - 1;
            break;
        case "MMM":
        case "MMMM":
            d = Q(c._l).monthsParse(b),
            d != null ? f[1] = d: c._isValid = !1;
            break;
        case "D":
        case "DD":
        case "DDD":
        case "DDDD":
            b != null && (f[2] = ~~b);
            break;
        case "YY":
            f[0] = ~~b + (~~b > 68 ? 1900 : 2e3);
            break;
        case "YYYY":
        case "YYYYY":
            f[0] = ~~b;
            break;
        case "a":
        case "A":
            c._isPm = (b + "").toLowerCase() === "pm";
            break;
        case "H":
        case "HH":
        case "h":
        case "hh":
            f[3] = ~~b;
            break;
        case "m":
        case "mm":
            f[4] = ~~b;
            break;
        case "s":
        case "ss":
            f[5] = ~~b;
            break;
        case "S":
        case "SS":
        case "SSS":
            f[6] = ~~ (("0." + b) * 1e3);
            break;
        case "X":
            c._d = new Date(parseFloat(b) * 1e3);
            break;
        case "Z":
        case "ZZ":
            c._useUTC = !0,
            d = (b + "").match(x),
            d && d[1] && (c._tzh = ~~d[1]),
            d && d[2] && (c._tzm = ~~d[2]),
            d && d[0] === "+" && (c._tzh = -c._tzh, c._tzm = -c._tzm)
        }
        b == null && (c._isValid = !1)
    }
    function W(a) {
        var b, c, d = [];
        if (a._d) return;
        for (b = 0; b < 7; b++) a._a[b] = d[b] = a._a[b] == null ? b === 2 ? 1 : 0 : a._a[b];
        d[3] += a._tzh || 0,
        d[4] += a._tzm || 0,
        c = new Date(0),
        a._useUTC ? (c.setUTCFullYear(d[0], d[1], d[2]), c.setUTCHours(d[3], d[4], d[5], d[6])) : (c.setFullYear(d[0], d[1], d[2]), c.setHours(d[3], d[4], d[5], d[6])),
        a._d = c
    }
    function X(a) {
        var b = a._f.match(i),
        c = a._i,
        d,
        e;
        a._a = [];
        for (d = 0; d < b.length; d++) e = (U(b[d]).exec(c) || [])[0],
        e && (c = c.slice(c.indexOf(e) + e.length)),
        D[b[d]] && V(b[d], e, a);
        a._isPm && a._a[3] < 12 && (a._a[3] += 12),
        a._isPm === !1 && a._a[3] === 12 && (a._a[3] = 0),
        W(a)
    }
    function Y(a) {
        var b, c, d, e = 99,
        f, g, h;
        while (a._f.length) {
            b = J({},
            a),
            b._f = a._f.pop(),
            X(b),
            c = new H(b);
            if (c.isValid()) {
                d = c;
                break
            }
            h = O(b._a, c.toArray()),
            h < e && (e = h, d = c)
        }
        J(a, d)
    }
    function Z(a) {
        var b, c = a._i;
        if (u.exec(c)) {
            a._f = "YYYY-MM-DDT";
            for (b = 0; b < 4; b++) if (w[b][1].exec(c)) {
                a._f += w[b][0];
                break
            }
            r.exec(c) && (a._f += " Z"),
            X(a)
        } else a._d = new Date(c)
    }
    function $(b) {
        var c = b._i,
        d = h.exec(c);
        c === a ? b._d = new Date: d ? b._d = new Date( + d[1]) : typeof c == "string" ? Z(b) : N(c) ? (b._a = c.slice(0), W(b)) : b._d = c instanceof Date ? new Date( + c) : new Date(c)
    }
    function _(a, b, c, d, e) {
        return e.relativeTime(b || 1, !!c, a, d)
    }
    function ba(a, b, c) {
        var e = d(Math.abs(a) / 1e3),
        f = d(e / 60),
        g = d(f / 60),
        h = d(g / 24),
        i = d(h / 365),
        j = e < 45 && ["s", e] || f === 1 && ["m"] || f < 45 && ["mm", f] || g === 1 && ["h"] || g < 22 && ["hh", g] || h === 1 && ["d"] || h <= 25 && ["dd", h] || h <= 45 && ["M"] || h < 345 && ["MM", d(h / 30)] || i === 1 && ["y"] || ["yy", i];
        return j[2] = b,
        j[3] = a > 0,
        j[4] = c,
        _.apply({},
        j)
    }
    function bb(a, c, d) {
        var e = d - c,
        f = d - a.day();
        return f > e && (f -= 7),
        f < e - 7 && (f += 7),
        Math.ceil(b(a).add("d", f).dayOfYear() / 7)
    }
    function bc(a) {
        var c = a._i,
        d = a._f;
        return c === null || c === "" ? null: (typeof c == "string" && (a._i = c = Q().preparse(c)), b.isMoment(c) ? (a = J({},
        c), a._d = new Date( + c._d)) : d ? N(d) ? Y(a) : X(a) : $(a), new H(a))
    }
    function bd(a, c) {
        b.fn[a] = b.fn[a + "s"] = function(a) {
            var b = this._isUTC ? "UTC": "";
            return a != null ? (this._d["set" + b + c](a), this) : this._d["get" + b + c]()
        }
    }
    function be(a) {
        b.duration.fn[a] = function() {
            return this._data[a]
        }
    }
    function bf(a, c) {
        b.duration.fn["as" + a] = function() {
            return + this / c
        }
    }
    var b, c = "2.0.0",
    d = Math.round,
    e, f = {},
    g = typeof module != "undefined" && module.exports,
    h = /^\/?Date\((\-?\d+)/i,
    i = /(\[[^\[]*\])|(\\)?(Mo|MM?M?M?|Do|DDDo|DD?D?D?|ddd?d?|do?|w[o|w]?|W[o|W]?|YYYYY|YYYY|YY|a|A|hh?|HH?|mm?|ss?|SS?S?|X|zz?|ZZ?|.)/g,
    j = /(\[[^\[]*\])|(\\)?(LT|LL?L?L?|l{1,4})/g,
    k = /([0-9a-zA-Z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)/gi,
    l = /\d\d?/,
    m = /\d{1,3}/,
    n = /\d{3}/,
    o = /\d{1,4}/,
    p = /[+\-]?\d{1,6}/,
    q = /[0-9]*[a-z\u00A0-\u05FF\u0700-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+|[\u0600-\u06FF]+\s*?[\u0600-\u06FF]+/i,
    r = /Z|[\+\-]\d\d:?\d\d/i,
    s = /T/i,
    t = /[\+\-]?\d+(\.\d{1,3})?/,
    u = /^\s*\d{4}-\d\d-\d\d((T| )(\d\d(:\d\d(:\d\d(\.\d\d?\d?)?)?)?)?([\+\-]\d\d:?\d\d)?)?/,
    v = "YYYY-MM-DDTHH:mm:ssZ",
    w = [["HH:mm:ss.S", /(T| )\d\d:\d\d:\d\d\.\d{1,3}/], ["HH:mm:ss", /(T| )\d\d:\d\d:\d\d/], ["HH:mm", /(T| )\d\d:\d\d/], ["HH", /(T| )\d\d/]],
    x = /([\+\-]|\d\d)/gi,
    y = "Month|Date|Hours|Minutes|Seconds|Milliseconds".split("|"),
    z = {
        Milliseconds: 1,
        Seconds: 1e3,
        Minutes: 6e4,
        Hours: 36e5,
        Days: 864e5,
        Months: 2592e6,
        Years: 31536e6
    },
    A = {},
    B = "DDD w W M D d".split(" "),
    C = "M D H h m s w W".split(" "),
    D = {
        M: function() {
            return this.month() + 1
        },
        MMM: function(a) {
            return this.lang().monthsShort(this, a)
        },
        MMMM: function(a) {
            return this.lang().months(this, a)
        },
        D: function() {
            return this.date()
        },
        DDD: function() {
            return this.dayOfYear()
        },
        d: function() {
            return this.day()
        },
        dd: function(a) {
            return this.lang().weekdaysMin(this, a)
        },
        ddd: function(a) {
            return this.lang().weekdaysShort(this, a)
        },
        dddd: function(a) {
            return this.lang().weekdays(this, a)
        },
        w: function() {
            return this.week()
        },
        W: function() {
            return this.isoWeek()
        },
        YY: function() {
            return L(this.year() % 100, 2)
        },
        YYYY: function() {
            return L(this.year(), 4)
        },
        YYYYY: function() {
            return L(this.year(), 5)
        },
        a: function() {
            return this.lang().meridiem(this.hours(), this.minutes(), !0)
        },
        A: function() {
            return this.lang().meridiem(this.hours(), this.minutes(), !1)
        },
        H: function() {
            return this.hours()
        },
        h: function() {
            return this.hours() % 12 || 12
        },
        m: function() {
            return this.minutes()
        },
        s: function() {
            return this.seconds()
        },
        S: function() {
            return~~ (this.milliseconds() / 100)
        },
        SS: function() {
            return L(~~ (this.milliseconds() / 10), 2)
        },
        SSS: function() {
            return L(this.milliseconds(), 3)
        },
        Z: function() {
            var a = -this.zone(),
            b = "+";
            return a < 0 && (a = -a, b = "-"),
            b + L(~~ (a / 60), 2) + ":" + L(~~a % 60, 2)
        },
        ZZ: function() {
            var a = -this.zone(),
            b = "+";
            return a < 0 && (a = -a, b = "-"),
            b + L(~~ (10 * a / 6), 4)
        },
        X: function() {
            return this.unix()
        }
    };
    while (B.length) e = B.pop(),
    D[e + "o"] = F(D[e]);
    while (C.length) e = C.pop(),
    D[e + e] = E(D[e], 2);
    D.DDDD = E(D.DDD, 3),
    G.prototype = {
        set: function(a) {
            var b, c;
            for (c in a) b = a[c],
            typeof b == "function" ? this[c] = b: this["_" + c] = b
        },
        _months: "January_February_March_April_May_June_July_August_September_October_November_December".split("_"),
        months: function(a) {
            return this._months[a.month()]
        },
        _monthsShort: "Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),
        monthsShort: function(a) {
            return this._monthsShort[a.month()]
        },
        monthsParse: function(a) {
            var c, d, e, f;
            this._monthsParse || (this._monthsParse = []);
            for (c = 0; c < 12; c++) {
                this._monthsParse[c] || (d = b([2e3, c]), e = "^" + this.months(d, "") + "|^" + this.monthsShort(d, ""), this._monthsParse[c] = new RegExp(e.replace(".", ""), "i"));
                if (this._monthsParse[c].test(a)) return c
            }
        },
        _weekdays: "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),
        weekdays: function(a) {
            return this._weekdays[a.day()]
        },
        _weekdaysShort: "Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),
        weekdaysShort: function(a) {
            return this._weekdaysShort[a.day()]
        },
        _weekdaysMin: "Su_Mo_Tu_We_Th_Fr_Sa".split("_"),
        weekdaysMin: function(a) {
            return this._weekdaysMin[a.day()]
        },
        _longDateFormat: {
            LT: "h:mm A",
            L: "MM/DD/YYYY",
            LL: "MMMM D YYYY",
            LLL: "MMMM D YYYY LT",
            LLLL: "dddd, MMMM D YYYY LT"
        },
        longDateFormat: function(a) {
            var b = this._longDateFormat[a];
            return ! b && this._longDateFormat[a.toUpperCase()] && (b = this._longDateFormat[a.toUpperCase()].replace(/MMMM|MM|DD|dddd/g,
            function(a) {
                return a.slice(1)
            }), this._longDateFormat[a] = b),
            b
        },
        meridiem: function(a, b, c) {
            return a > 11 ? c ? "pm": "PM": c ? "am": "AM"
        },
        _calendar: {
            sameDay: "[Today at] LT",
            nextDay: "[Tomorrow at] LT",
            nextWeek: "dddd [at] LT",
            lastDay: "[Yesterday at] LT",
            lastWeek: "[last] dddd [at] LT",
            sameElse: "L"
        },
        calendar: function(a, b) {
            var c = this._calendar[a];
            return typeof c == "function" ? c.apply(b) : c
        },
        _relativeTime: {
            future: "in %s",
            past: "%s ago",
            s: "a few seconds",
            m: "a minute",
            mm: "%d minutes",
            h: "an hour",
            hh: "%d hours",
            d: "a day",
            dd: "%d days",
            M: "a month",
            MM: "%d months",
            y: "a year",
            yy: "%d years"
        },
        relativeTime: function(a, b, c, d) {
            var e = this._relativeTime[c];
            return typeof e == "function" ? e(a, b, c, d) : e.replace(/%d/i, a)
        },
        pastFuture: function(a, b) {
            var c = this._relativeTime[a > 0 ? "future": "past"];
            return typeof c == "function" ? c(b) : c.replace(/%s/i, b)
        },
        ordinal: function(a) {
            return this._ordinal.replace("%d", a)
        },
        _ordinal: "%d",
        preparse: function(a) {
            return a
        },
        postformat: function(a) {
            return a
        },
        week: function(a) {
            return bb(a, this._week.dow, this._week.doy)
        },
        _week: {
            dow: 0,
            doy: 6
        }
    },
    b = function(a, b, c) {
        return bc({
            _i: a,
            _f: b,
            _l: c,
            _isUTC: !1
        })
    },
    b.utc = function(a, b, c) {
        return bc({
            _useUTC: !0,
            _isUTC: !0,
            _l: c,
            _i: a,
            _f: b
        })
    },
    b.unix = function(a) {
        return b(a * 1e3)
    },
    b.duration = function(a, c) {
        var d = b.isDuration(a),
        e = typeof a == "number",
        f = d ? a._data: e ? {}: a,
        g;
        return e && (c ? f[c] = a: f.milliseconds = a),
        g = new I(f),
        d && a.hasOwnProperty("_lang") && (g._lang = a._lang),
        g
    },
    b.version = c,
    b.defaultFormat = v,
    b.lang = function(a, c) {
        var d;
        if (!a) return b.fn._lang._abbr;
        c ? P(a, c) : f[a] || Q(a),
        b.duration.fn._lang = b.fn._lang = Q(a)
    },
    b.langData = function(a) {
        return a && a._lang && a._lang._abbr && (a = a._lang._abbr),
        Q(a)
    },
    b.isMoment = function(a) {
        return a instanceof H
    },
    b.isDuration = function(a) {
        return a instanceof I
    },
    b.fn = H.prototype = {
        clone: function() {
            return b(this)
        },
        valueOf: function() {
            return + this._d
        },
        unix: function() {
            return Math.floor( + this._d / 1e3)
        },
        toString: function() {
            return this.format("ddd MMM DD YYYY HH:mm:ss [GMT]ZZ")
        },
        toDate: function() {
            return this._d
        },
        toJSON: function() {
            return b.utc(this).format("YYYY-MM-DD[T]HH:mm:ss.SSS[Z]")
        },
        toArray: function() {
            var a = this;
            return [a.year(), a.month(), a.date(), a.hours(), a.minutes(), a.seconds(), a.milliseconds()]
        },
        isValid: function() {
            return this._isValid == null && (this._a ? this._isValid = !O(this._a, (this._isUTC ? b.utc(this._a) : b(this._a)).toArray()) : this._isValid = !isNaN(this._d.getTime())),
            !!this._isValid
        },
        utc: function() {
            return this._isUTC = !0,
            this
        },
        local: function() {
            return this._isUTC = !1,
            this
        },
        format: function(a) {
            var c = T(this, a || b.defaultFormat);
            return this.lang().postformat(c)
        },
        add: function(a, c) {
            var d;
            return typeof a == "string" ? d = b.duration( + c, a) : d = b.duration(a, c),
            M(this, d, 1),
            this
        },
        subtract: function(a, c) {
            var d;
            return typeof a == "string" ? d = b.duration( + c, a) : d = b.duration(a, c),
            M(this, d, -1),
            this
        },
        diff: function(a, c, d) {
            var e = this._isUTC ? b(a).utc() : b(a).local(),
            f = (this.zone() - e.zone()) * 6e4,
            g,
            h;
            return c && (c = c.replace(/s$/, "")),
            c === "year" || c === "month" ? (g = (this.daysInMonth() + e.daysInMonth()) * 432e5, h = (this.year() - e.year()) * 12 + (this.month() - e.month()), h += (this - b(this).startOf("month") - (e - b(e).startOf("month"))) / g, c === "year" && (h /= 12)) : (g = this - e - f, h = c === "second" ? g / 1e3: c === "minute" ? g / 6e4: c === "hour" ? g / 36e5: c === "day" ? g / 864e5: c === "week" ? g / 6048e5: g),
            d ? h: K(h)
        },
        from: function(a, c) {
            return b.duration(this.diff(a)).lang(this.lang()._abbr).humanize(!c)
        },
        fromNow: function(a) {
            return this.from(b(), a)
        },
        calendar: function() {
            var a = this.diff(b().startOf("day"), "days", !0),
            c = a < -6 ? "sameElse": a < -1 ? "lastWeek": a < 0 ? "lastDay": a < 1 ? "sameDay": a < 2 ? "nextDay": a < 7 ? "nextWeek": "sameElse";
            return this.format(this.lang().calendar(c, this))
        },
        isLeapYear: function() {
            var a = this.year();
            return a % 4 === 0 && a % 100 !== 0 || a % 400 === 0
        },
        isDST: function() {
            return this.zone() < b([this.year()]).zone() || this.zone() < b([this.year(), 5]).zone()
        },
        day: function(a) {
            var b = this._isUTC ? this._d.getUTCDay() : this._d.getDay();
            return a == null ? b: this.add({
                d: a - b
            })
        },
        startOf: function(a) {
            a = a.replace(/s$/, "");
            switch (a) {
            case "year":
                this.month(0);
            case "month":
                this.date(1);
            case "week":
            case "day":
                this.hours(0);
            case "hour":
                this.minutes(0);
            case "minute":
                this.seconds(0);
            case "second":
                this.milliseconds(0)
            }
            return a === "week" && this.day(0),
            this
        },
        endOf: function(a) {
            return this.startOf(a).add(a.replace(/s?$/, "s"), 1).subtract("ms", 1)
        },
        isAfter: function(a, c) {
            return c = typeof c != "undefined" ? c: "millisecond",
            +this.clone().startOf(c) > +b(a).startOf(c)
        },
        isBefore: function(a, c) {
            return c = typeof c != "undefined" ? c: "millisecond",
            +this.clone().startOf(c) < +b(a).startOf(c)
        },
        isSame: function(a, c) {
            return c = typeof c != "undefined" ? c: "millisecond",
            +this.clone().startOf(c) === +b(a).startOf(c)
        },
        zone: function() {
            return this._isUTC ? 0 : this._d.getTimezoneOffset()
        },
        daysInMonth: function() {
            return b.utc([this.year(), this.month() + 1, 0]).date()
        },
        dayOfYear: function(a) {
            var c = d((b(this).startOf("day") - b(this).startOf("year")) / 864e5) + 1;
            return a == null ? c: this.add("d", a - c)
        },
        isoWeek: function(a) {
            var b = bb(this, 1, 4);
            return a == null ? b: this.add("d", (a - b) * 7)
        },
        week: function(a) {
            var b = this.lang().week(this);
            return a == null ? b: this.add("d", (a - b) * 7)
        },
        lang: function(b) {
            return b === a ? this._lang: (this._lang = Q(b), this)
        }
    };
    for (e = 0; e < y.length; e++) bd(y[e].toLowerCase().replace(/s$/, ""), y[e]);
    bd("year", "FullYear"),
    b.fn.days = b.fn.day,
    b.fn.weeks = b.fn.week,
    b.fn.isoWeeks = b.fn.isoWeek,
    b.duration.fn = I.prototype = {
        weeks: function() {
            return K(this.days() / 7)
        },
        valueOf: function() {
            return this._milliseconds + this._days * 864e5 + this._months * 2592e6
        },
        humanize: function(a) {
            var b = +this,
            c = ba(b, !a, this.lang());
            return a && (c = this.lang().pastFuture(b, c)),
            this.lang().postformat(c)
        },
        lang: b.fn.lang
    };
    for (e in z) z.hasOwnProperty(e) && (bf(e, z[e]), be(e.toLowerCase()));
    bf("Weeks", 6048e5),
    b.lang("en", {
        ordinal: function(a) {
            var b = a % 10,
            c = ~~ (a % 100 / 10) === 1 ? "th": b === 1 ? "st": b === 2 ? "nd": b === 3 ? "rd": "th";
            return a + c
        }
    }),
    g && (module.exports = b),
    typeof ender == "undefined" && (this.moment = b),
    typeof define == "function" && define.amd && define("moment", [],
    function() {
        return b
    })
}.call(this),
function(a) {
    a(function() {
        moment.lang("zh-cn", {
            months: "一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月".split("_"),
            monthsShort: "1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),
            weekdays: "星期日_星期一_星期二_星期三_星期四_星期五_星期六".split("_"),
            weekdaysShort: "周日_周一_周二_周三_周四_周五_周六".split("_"),
            weekdaysMin: "日_一_二_三_四_五_六".split("_"),
            longDateFormat: {
                LT: "Ah点mm",
                L: "YYYY年MMMD日",
                LL: "YYYY年MMMD日",
                LLL: "YYYY年MMMD日LT",
                LLLL: "YYYY年MMMD日ddddLT",
                l: "YYYY年MMMD日",
                ll: "YYYY年MMMD日",
                lll: "YYYY年MMMD日LT",
                llll: "YYYY年MMMD日ddddLT"
            },
            meridiem: function(a, b, c) {
                return a < 9 ? "早上": a < 11 && b < 30 ? "上午": a < 13 && b < 30 ? "中午": a < 18 ? "下午": "晚上"
            },
            calendar: {
                sameDay: "[今天]LT",
                nextDay: "[明天]LT",
                nextWeek: "[下]ddddLT",
                lastDay: "[昨天]LT",
                lastWeek: "[上]ddddLT",
                sameElse: "L"
            },
            relativeTime: {
                future: "%s内",
                past: "%s前",
                s: "几秒",
                m: "1分钟",
                mm: "%d分钟",
                h: "1小时",
                hh: "%d小时",
                d: "1天",
                dd: "%d天",
                M: "1个月",
                MM: "%d个月",
                y: "1年",
                yy: "%d年"
            },
            week: {
                dow: 1
            }
        }),
        a.ajaxSetup({
            type: "POST",
            dataType: "json",
            data: {
                conn_guid: a("#conn-guid").val()
            },
            beforeSend: function(b, c) {
                if (c.type != "GET") {
                    var d = a("meta[name='csrf-token']").attr("content");
                    b.setRequestHeader("X-CSRF-Token", d)
                }
            },
            error: function(b, c, d) {
                if (c === "abort") return;
                var e = a.parseJSON(b.responseText),
                f = "";
                if (!e || !e.errors && !e.msg) return;
                e.errors ? a.each(e.errors,
                function(a, b) {
                    f += b.msg + "<br/>"
                }) : f += e.msg,
                f && mcw.message({
                    msg: f
                });
                var g = mcw.urlParts(location.href).href;
                mcw.clearPageCache(g)
            }
        }),
        a.rails && a("body").on("keydown", "form.form[data-remote=true] textarea",
        function(b) {
            var c = mcw.metaKey(b);
            c && b.which == 13 && (b.preventDefault(), a(this).closest("form.form").submit())
        }).on("submit", "form.form",
        function(b) {
            var c = a(b.currentTarget),
            d = !0,
            e = ["input[data-validate]:visible", "textarea[data-validate]:visible", ".mcw-editor textarea[data-validate]"].join(",");
            return c.find(e).each(function(b, c) {
                mcw.validateField(a(c)) || (d = !1)
            }),
            d
        }).on("blur.validate", "input[data-validate]",
        function(b) {
            var c = a(this);
            c.attr("data-blur-validate") == "true" && mcw.validateField(c, !0)
        }).on("ajax:error", "form.form[data-remote=true]",
        function(b, c) {
            var d = a(b.currentTarget),
            e = a.parseJSON(c.responseText).errors;
            a.each(e,
            function(b, c) {
                var e = d.find("input[name=" + c.target + "], textarea[name=" + c.target + "]"),
                f = e.nextAll(".error");
                f.length || (f = a("<p class='error'></p>").insertAfter(e), f.parent(".mcw-editor").addClass("error")),
                f.text(c.msg),
                e.addClass("error").nextAll(".desc").hide()
            })
        }).on("ajax:beforeSend", "form.form[data-remote=true]",
        function(b, c, d) {
            var e = a(this).find("button[type=submit]");
            e.is("[data-global-loading]") ? mcw.globalLoading(e.data("global-loading")) : e.is("[data-loading]") && mcw.tinyLoading(e)
        }).on("ajax:complete", "form.form[data-remote=true]",
        function(b, c, d) {
            var e = a(this).find("button[type=submit]");
            e.is("[data-global-loading]") ? mcw.globalLoading("hide") : e.is("[data-loading]") && mcw.tinyLoading(link, !1);
            if (d == "success") {
                var f = a(this).find(a.rails.enableSelector),
                g = f.attr("data-success-text"),
                h = a.parseJSON(c.responseText),
                i = h && h.target_url || f.attr("data-goto"),
                j = f.data("refresh");
                g && f.text(g + " ✓").prop("disabled", !0).addClass("success");
                if (i) {
                    var k = mcw.urlParts(i),
                    l = mcw.urlParts(location.href);
                    k.path != l.path && (a(".workspace").length ? mcw.stack({
                        url: i,
                        replace: !0,
                        root: f.is("[data-goto-root]"),
                        restorePosition: !0
                    }) : location.href = i)
                }
                j && mcw.stack({
                    url: location.href,
                    nocache: !0
                }),
                g && !i && !j && setTimeout(function() {
                    f.text(f.data("ujs:enable-with")).prop("disabled", !1).removeClass("success")
                },
                3e3);
                if (g || i || j) return ! 1
            }
        }).on("ajax:complete", a.rails.linkClickSelector,
        function(b, c, d) {
            var e = a(this);
            e.is("[data-global-loading]") ? mcw.globalLoading("hide") : e.is("[data-loading]") && mcw.tinyLoading(e, !1),
            e.is(".btn[data-disable-with]") && e.text(e.data("ujs:enable-with")).prop("disabled", !1);
            if (d == "success") {
                var f = a.parseJSON(c.responseText),
                g = f && f.target_url || e.attr("data-goto"),
                h = e.data("refresh");
                if (g) {
                    var i = mcw.urlParts(g),
                    j = mcw.urlParts(location.href);
                    if (i.path != j.path) if (a(".workspace").length) {
                        var k = !0;
                        e.is("[data-stack-replace]") && e.data("stack-replace") == 0 && (k = !1),
                        mcw.stack({
                            url: g,
                            replace: k,
                            root: e.is("[data-goto-root]"),
                            restorePosition: !0,
                            bare: e.is("[data-goto-bare]")
                        })
                    } else location.href = g
                }
                h && mcw.stack({
                    url: location.href,
                    nocache: !0
                })
            }
        }).on("ajax:error", a.rails.linkClickSelector,
        function(b, c, d, e) {
            if (d === "abort") return;
            var f = a.parseJSON(c.responseText),
            g = "";
            f.errors ? a.each(f.errors,
            function(a, b) {
                g += b.msg + "<br/>"
            }) : g += f.msg,
            mcw.message({
                msg: g
            })
        }).on("ajax:beforeSend", a.rails.linkClickSelector,
        function(b, c, d) {
            var e = a(this);
            e.is("[data-global-loading]") ? mcw.globalLoading(e.data("global-loading")) : e.is("[data-loading]") && mcw.tinyLoading(e)
        }),
        mcw.lastUpdated = moment()
    }),
    window.mcw = {
        now: function() {
            var b = a("#server-time").val();
            if (b) b = moment(b, "YYYY-MM-DD HH:mm:ss Z");
            else return moment();
            return b.add("ms", moment().diff(mcw.lastUpdated))
        },
        loadImage: function(a, b) {
            var c = new Image;
            b && (c.onload = function() {
                b(c)
            },
            c.onerror = function() {
                b()
            });
            if (typeof a == "string") c.src = a;
            else if (a.nodeName && a.nodeName == "IMG") c.src = a.src;
            else if (window.FileReader && FileReader.prototype.readAsDataURL) {
                var d = new FileReader;
                d.onload = function(a) {
                    c.src = a.target.result
                },
                d.readAsDataURL(a)
            } else b()
        },
        preloadImages: function(b) {
            a.each(b,
            function(a, b) {
                mcw.loadImage(b)
            })
        },
        truncate: function(a, b) {
            return a.length > b ? a.substring(0, b - 1) + "...": a
        },
        encodeHtml: function(a) {
            return (a + "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&#39;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        },
        decodeHtml: function(a) {
            return (a + "").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&")
        },
        template: function(b, c) {
            var d = a.trim(a("#" + b).html());
            return c && a.each(c,
            function(a, b) {
                var c = new RegExp("\\{\\{ " + a + " \\}\\}", "g");
                d = d.replace(c, mcw.encodeHtml(b))
            }),
            a(d)
        },
        params: function(a) {
            a = a.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var b = "[\\?&]" + a + "=([^&#]*)",
            c = new RegExp(b),
            d = c.exec(window.location.search);
            return d ? decodeURIComponent(d[1].replace(/\+/g, " ")) : ""
        },
        parseParams: function(a) {
            if (!a) return null;
            var b = /([^&=]+)=?([^&]*)/g,
            c = /\+/g,
            d = function(a) {
                return decodeURIComponent(a.replace(c, " "))
            };
            params = {},
            e;
            while (e = b.exec(a)) {
                var f = d(e[1]),
                g = d(e[2]);
                f.substring(f.length - 2) === "[]" ? (f = f.substring(0, f.length - 2), (params[f] || (params[f] = [])).push(g)) : params[f] = g
            }
            return params
        },
        urlParts: function(b) {
            if (!b) return null;
            var c = a("<a/>", {
                href: b
            }),
            d = "/" + c[0].pathname.replace(/\/$/g, "").replace(/^\//g, "") + "/",
            e = c[0].search,
            f = c[0].hash;
            return {
                href: d + e + f,
                path: d,
                search: e,
                hash: f
            }
        },
        supportTransition: function() {
            var a = document.body || document.documentElement,
            b = a.style,
            c = "transition";
            if (typeof b[c] == "string") return ! 0;
            v = ["Moz", "Webkit", "Khtml", "O", "ms"],
            c = c.charAt(0).toUpperCase() + c.substr(1);
            for (var d = 0; d < v.length; d++) if (typeof b[v[d] + c] == "string") return ! 0;
            return ! 1
        },
        transitionEnd: function(b, c) {
            if (mcw.supportTransition()) {
                var d = "transitionend";
                a.browser.webkit ? d = "webkitTransitionEnd": a.browser.msie ? d = "transitionend": a.browser.opera && (d = "oTransitionEnd"),
                b.one(d, c);
            } else setTimeout(c, 200)
        },
        dialog: function() {
            if (typeof arguments[0] == "string" && arguments[0] == "hide") return a(document).off(".dialog"),
            a("#mask").remove(),
            a(".dialog").remove();
            if (typeof arguments[0] == "object") {
                var b = a.extend({
                    el: null,
                    width: 600,
                    height: "auto",
                    modal: !1,
                    padding: !0,
                    closeButton: !0
                },
                arguments[0]);
                mcw.dialog("hide");
                var c = a("<div class='dialog'><div class='dialog-wrapper clearfix'></div><a href='javascript:;' class='link-close-dialog'>Close</a></div>").css({
                    width: b.width,
                    height: b.height
                }).appendTo(".page:last");
                b.closeButton || c.find(".link-close-dialog").remove(),
                c.find(".dialog-wrapper").append(b.el),
                c.find(".link-close-dialog").on("click",
                function(a) {
                    a.preventDefault(),
                    mcw.dialog("hide")
                }),
                a(document).on("keydown.dialog",
                function(a) {
                    a.which == 27 && mcw.dialog("hide")
                }),
                setTimeout(function() {
                    c.css({
                        marginLeft: -b.width / 2,
                        marginTop: -c.height() / 2
                    })
                },
                20);
                if (b.modal) {
                    var d = a("<div id='mask' class='hidden'></div>").appendTo(".page:last");
                    d.on("click",
                    function(a) {
                        mcw.dialog("hide")
                    }),
                    setTimeout(function() {
                        d.removeClass("hidden")
                    },
                    20)
                }
                return c
            }
            return null
        },
        message: function(b) {
            var c = a("<div class='message-content'><p></p><div class='dialog-buttons clearfix'><button class='btn'></button></div></div>");
            c.find("p").html(b.msg),
            c.find(".dialog-buttons button").text(b.ok || "我知道了").on("click",
            function(a) {
                mcw.dialog("hide")
            }),
            mcw.dialog(a.extend({
                el: c,
                width: 450
            },
            b))
        },
        confirm: function(b) {
            var c = a("<div class='message-content'><p></p><div class='dialog-buttons clearfix'><button class='btn btn-primary btn-yes'></button><a href='javascript:void(0)' class='link-no'></a></div></div>");
            c.find("p").html(b.msg),
            c.find(".dialog-buttons .btn-yes").text(b.ok || "确定").on("click",
            function(a) {
                mcw.dialog("hide"),
                b.callback(!0, a)
            }),
            c.find(".dialog-buttons .link-no").text(b.cancel || "取消").on("click",
            function(a) {
                a.preventDefault(),
                mcw.dialog("hide"),
                b.callback(!1, a)
            }),
            mcw.dialog(a.extend({
                el: c,
                width: 450
            },
            b))
        },
        globalLoading: function(b) {
            if (b == "hide") a("#mask, .global-loading").remove();
            else {
                var c = a("<div id='mask' class='hidden'></div>").appendTo("body"),
                d = a("<div class='global-loading'>" + b + "</div>").appendTo("body");
                setTimeout(function() {
                    c && c.css({
                        cursor: "default"
                    }).removeClass("hidden"),
                    d && d.css({
                        marginLeft: -d.outerWidth() * .5,
                        marginTop: -d.outerHeight() * .5
                    })
                },
                20)
            }
        },
        tinyLoading: function(b, c) {
            b = a(b);
            if (c !== !1) {
                var d = a("<img />", {
                    src: "/static/classic/images/blank-3dbe121a376a181f0fe840fb1daeeb51.gif"
                }).css({
                    display: b.css("display"),
                    width: b.outerWidth(),
                    height: b.outerHeight(),
                    marginLeft: b.css("marginLeft"),
                    marginTop: b.css("marginTop"),
                    marginRight: b.css("marginRight"),
                    marginBottom: b.css("marginBottom"),
                    "float": b.css("float"),
                    position: b.css("position"),
                    verticalAlign: "middle",
                    background: "url(/static/classic/images/tiny-loading-e8bd9af828c29751e76f3d73d4f9e005.gif) no-repeat 50% 50%"
                }).addClass("tiny-loading").insertAfter(b),
                e = b.css("top"),
                f = b.css("left"),
                g = b.css("right"),
                h = b.css("bottom"); ! e || e == "auto" ? d.css("bottom", h) : d.css("top", e),
                !f || f == "auto" ? d.css("right", g) : d.css("left", f),
                b.hide()
            } else b.next(".tiny-loading").remove(),
            b.show()
        },
        selectText: function(b, c, d) {
            b = a(b);
            if (!a.isNumeric(c) || c < 0) c = b.val().length;
            d = d || c;
            if (b[0].createTextRange) {
                var e = b[0].createTextRange();
                e.collapse(!0),
                e.moveStart("character", c),
                e.moveEnd("character", d),
                e.select()
            } else b[0].setSelectionRange && b[0].setSelectionRange(c, c + d);
            b.focus()
        },
        tooltip: function(b, c) {
            if (navigator.platform.indexOf("iPhone") != -1 || navigator.platform.indexOf("iPod") != -1 || navigator.platform.indexOf("iPad") != -1) return;
            if (c == "hide") {
                var d = b.data("tooltipTimer"),
                e = b.data("tooltipEl");
                d && (clearTimeout(d), d = null),
                e && (e.remove(), e = null)
            } else {
                var d = b.data("tooltipTimer"),
                e = b.data("tooltipEl"),
                f = b.offset(),
                g = b.width(),
                h = b.height(),
                i = b.attr("tooltip");
                d && (clearTimeout(d), d = null),
                e && (e.remove(), e = null),
                e = a("<div class='tooltip'><div class='tooltip-arrow'></div><div class='tooltip-content'></div></div>").appendTo("body"),
                e.find(".tooltip-content").text(i),
                e.css({
                    opacity: 0,
                    top: f.top + h,
                    left: f.left - (e.width() - g) * .5
                }),
                d = setTimeout(function() {
                    e.addClass("transition").css({
                        opacity: 1,
                        top: f.top + h + 15
                    })
                },
                200),
                b.data("tooltipTimer", d),
                b.data("tooltipEl", e)
            }
        },
        fitSize: function(b, c, d) {
            d = a.extend({
                stretch: !1,
                minWidth: 0,
                minHeight: 0
            },
            d);
            var e = {
                width: c.width,
                height: c.height
            };
            if (d.stretch || c.width > b.width || c.height > b.height || c.width < d.minWidth || c.height < d.minHeight) c.width / c.height > b.width / b.height ? (e.width = Math.max(b.width, d.minWidth), e.height = e.width * c.height / c.width) : (e.height = Math.max(b.height, d.minHeight), e.width = e.height * c.width / c.height);
            return e.x = (b.width - e.width) / 2,
            e.y = (b.height - e.height) / 2,
            e
        },
        viewImage: function(b) {
            function r(b, c) {
                if (!l) return;
                var d = a(window),
                e = mcw.fitSize({
                    width: d.width() - 80,
                    height: d.height() - (p.length > 1 ? 160 : 80)
                },
                c || {
                    width: b.width,
                    height: b.height
                });
                e.x += 40,
                e.y += 30,
                l.css({
                    width: e.width,
                    height: e.height,
                    top: e.y,
                    left: e.x
                }).find("img").attr({
                    src: b.src
                }),
                l.removeClass("loading"),
                n.show()
            }
            function s() {
                n.hide();
                var b = a(document).scrollTop(),
                d = a(document).scrollLeft(),
                e = {
                    width: c.width(),
                    height: c.height(),
                    top: c.offset().top - b,
                    left: c.offset().left - d
                };
                l.css(e),
                mcw.transitionEnd(l,
                function(a) {
                    j.trigger("galleryhide").remove(),
                    l = null
                }),
                a(document).unbind(".originimg")
            }
            var c = b,
            d = b.data("origin-src"),
            e = b.data("origin-size"),
            f = b.data("origin-name");
            if (!d) return;
            c.is("[src]") || (c = c.find("[src]:first")),
            e ? (e = e.split(","), e = {
                width: e[0] * 1 || c.width() * 10,
                height: e[1] * 1 || c.height() * 10
            }) : e = {
                width: c.width() * 10,
                height: c.height() * 10
            };
            var g = a(document).scrollTop(),
            h = a(document).scrollLeft(),
            i = {
                width: c.width(),
                height: c.height(),
                top: c.offset().top - g,
                left: c.offset().left - h
            },
            j = a("<div />", {
                "class": "gallery-wrapper loading"
            }).click(a.proxy(s, this)).appendTo("body"),
            k = a("<div class='mask'></div>").appendTo(j),
            l = a("<div />", {
                id: "gallery-img"
            }).css({
                width: i.width,
                height: i.height,
                top: i.top,
                left: i.left
            }).appendTo(j),
            m = a("<img />", {
                src: c.attr("src")
            }).appendTo(l),
            n = a("<div />", {
                "class": "gallery-img-name hide",
                html: "<span>" + f + '</span> [ <a href="' + d + '" target="_blank">查看原图</a> ] '
            }).appendTo(l),
            o = a("<div />", {
                "class": "loading-indicator"
            }).appendTo(l),
            p = b.closest(".attachments, .attachments-preview").find("*[data-origin-src]"),
            q = null;
            return p.length > 1 && (q = a("<ul/>", {
                "class": "gallery"
            }).appendTo(j), p.each(function(b, d) {
                var e = a(d),
                f;
                e.is("[src]") ? f = e: f = e.find("[src]:first");
                var g = a("<li/>"),
                h = a("<a/>", {
                    href: "javascript:;"
                }).appendTo(g),
                i = a("<img/>", {
                    src: f.attr("src")
                }).appendTo(h);
                h.on("click", {
                    d: e,
                    t: f
                },
                function(a) {
                    var b = a.data.d,
                    d = a.data.t;
                    return c = d,
                    n.hide(),
                    h.parent("li").addClass("selected").siblings("li").removeClass("selected"),
                    n.find("span").text(b.data("origin-name")).end().find("a").attr("href", b.data("origin-src")),
                    l.addClass("loading"),
                    mcw.loadImage(b.data("origin-src"),
                    function(a) {
                        r(a)
                    }),
                    !1
                }),
                f[0] == c[0] && g.addClass("selected"),
                q.append(g)
            })),
            a(document).on("keydown.originimg", a.proxy(function(a) {
                if (/27|32/.test(a.which)) return s.call(this),
                !1;
                if (/37|38/.test(a.which)) return q.find(".selected").prev("li").find("a").click(),
                !1;
                if (/39|40/.test(a.which)) return q.find(".selected").next("li").find("a").click(),
                !1
            },
            this)),
            a("span, a", n).on("click",
            function(a) {
                a.stopPropagation()
            }),
            setTimeout(function() {
                mcw.loadImage(c.attr("src"),
                function(b) {
                    if (!b) return j.remove(),
                    !1;
                    mcw.transitionEnd(l,
                    function(b) {
                        j.trigger("galleryshow"),
                        l.addClass("loading"),
                        mcw.loadImage(d,
                        function(a) {
                            l.removeClass("loading").find("img").attr("src", a.src)
                        }),
                        q && q.css({
                            left: (a(window).width() - q.width()) / 2
                        }),
                        n.show()
                    }),
                    r(b, e),
                    n.hide(),
                    j.removeClass("loading")
                })
            },
            20),
            j
        },
        scrollTo: function(b, c) {
            c = a.extend({
                anim: !0,
                duration: 500,
                container: null,
                callback: a.noop
            },
            c);
            var d = null,
            e = c.container ? a(c.container) : a("html, body");
            if (typeof b != "object" || typeof b.top != "number" && typeof b.left != "number") {
                var f = a(b).offset(),
                g = e.offset() || {
                    top: 0,
                    left: 0
                };
                d = {
                    top: f.top - g.top - 30,
                    left: f.left - g.left - 30
                }
            } else d = b;
            c.anim ? e.animate({
                scrollLeft: d.left,
                scrollTop: d.top
            },
            c.duration, c.callback) : (e.scrollLeft(d.left).scrollTop(d.top), c.callback())
        },
        validateField: function(b, c) {
            var d = b.attr("data-validate"),
            e = b.attr("data-validate-msg"),
            f = b.val(),
            g = !0,
            h = "";
            if (d) d = d.split(";");
            else return g;
            e !== undefined && (e = e.split(";")),
            a.each(d,
            function(d, i) {
                var i = a.trim(i).split(":"),
                j = i[0],
                k = i.length > 1 ? i[1] : null,
                l = null;
                if (j == "custom") {
                    var m = a.Event("validate");
                    b.trigger(m, [f, k]),
                    l = m.result || {
                        valid: !0
                    }
                } else l = mcw.validate[j](f, k);
                if (!l.valid) return g = l.valid,
                e && e.length && e[d] ? h = e[d] : l.errorMsg ? h = l.errorMsg: h = "",
                j == "required" && c && (g = !0, h = ""),
                !1
            });
            if (!g) {
                b.addClass("error").nextAll(".desc").hide();
                if (h) {
                    var i = b.nextAll(".error");
                    i.length || (i = a("<p class='error'></p>").appendTo(b.parent())),
                    i.text(h).show()
                }
            } else b.removeClass("error").nextAll(".desc").show().end().nextAll(".error").remove();
            return g
        },
        validate: {
            required: function(b, c) {
                return {
                    valid: !!a.trim(b),
                    errorMsg: "请填写这个字段"
                }
            },
            length: function(a, b) {
                b = (b || "0").split(",");
                var c = a.length,
                d = b[0] * 1,
                e = b.length > 1 ? b[1] * 1 : null;
                return {
                    valid: !a || c >= d && (!e || c <= e),
                    errorMsg: "这个字段的长度不能" + (d > 0 ? "少于" + d + "位": "") + (e ? "多余" + e + "位": "")
                }
            },
            range: function(a, b) {
                b = (b || "0").split(",");
                var c = b[0] * 1,
                d = b.length > 1 ? b[1] * 1 : null;
                return {
                    valid: !a || a >= c && (!d || a <= d),
                    errorMsg: "这个字段的值" + (c > 0 ? "不能小于" + c: "") + (d ? "不能大余" + d: "")
                }
            },
            email: function(a, b) {
                var c = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return {
                    valid: !a || c.test(a),
                    errorMsg: "请填写正确的邮箱地址"
                }
            },
            number: function(a, b) {
                return {
                    valid: !a || /^\d+$/.test(a),
                    errorMsg: "请填写数字"
                }
            },
            mobile: function(a, b) {
                return {
                    valid: !a || /^\d{11}$/.test(a),
                    errorMsg: "请填写一个有效的手机号码"
                }
            }
        },
        popover: function(b, c) {
            function e() {
                a(".popover").each(function(b, c) {
                    mcw.popover(a(c).data("target"), "hide")
                })
            }
            function f(b, c) {
                var d = b.offset(),
                e = b.outerWidth(),
                f = b.outerHeight(),
                g = a(window).height(),
                h = a(window).width(),
                i = c.data("opts") || {},
                j = c.outerHeight(),
                k = c.outerWidth(),
                l = a(document).scrollTop(),
                m = a(document).scrollLeft(),
                n = i.arrowWidth,
                o = i.arrowHeight,
                p = 15,
                q,
                r;
                c.removeClass("direction-left-top direction-right-top").removeClass("direction-left-bottom direction-right-bottom").removeClass("direction-top-left direction-top-right").removeClass("direction-bottom-left direction-bottom-right"),
                i.position ? c.addClass("direction-" + i.position) : g - d.top - f + l < j + 10 ? h - d.left - e + m < k + 20 ? c.addClass("direction-left-top") : c.addClass("direction-right-top") : h - d.left - e + m < k + 20 ? c.addClass("direction-left-bottom") : c.addClass("direction-right-bottom"),
                c.hasClass("direction-left-top") ? (q = d.top + f / 2 + n / 2 + p - j, r = d.left - o - k) : c.hasClass("direction-right-top") ? (q = d.top + f / 2 + n / 2 + p - j, r = d.left + e + o) : c.hasClass("direction-left-bottom") ? (q = d.top + f / 2 - n / 2 - p, r = d.left - o - k) : c.hasClass("direction-right-bottom") ? (q = d.top + f / 2 - n / 2 - p, r = d.left + e + o) : c.hasClass("direction-top-left") ? (q = d.top - o - j, r = d.left + e / 2 + n / 2 + p - k) : c.hasClass("direction-top-right") ? (q = d.top - o - j, r = d.left + e / 2 - arrow / 2 - p) : c.hasClass("direction-bottom-left") ? (q = d.top + f + o, r = d.left + e / 2 + n / 2 + p - k) : c.hasClass("direction-bottom-right") && (q = d.top + f + o, r = d.left + e / 2 - n / 2 - p),
                i.offset && (q += i.offset.top, r += i.offset.left),
                c.css({
                    top: q,
                    left: r
                })
            }
            if (b == "clear") e();
            else if (c == "hide") {
                var d = a(b).data("popover");
                d && (d.remove(), a(b).removeClass("popover-target").data("popover", null), a(document).unbind(".popover").trigger("popoverhide", [b]))
            } else {
                if (c != "refresh") {
                    c = a.extend({
                        content: null,
                        position: null,
                        offset: null,
                        autohide: !0,
                        cls: null,
                        arrowWidth: 20,
                        arrowHeight: 10
                    },
                    c),
                    e(),
                    b = a(b);
                    var d = a("<div class='popover'>\t\t\t\t\t<div class='popover-content'></div>\t\t\t\t\t<div class='popover-arrow'></div>\t\t\t\t</div>");
                    return c.cls && d.addClass(c.cls),
                    d.appendTo("body").data("target", b).data("opts", c).find(".popover-content").append(c.content),
                    f(b, d),
                    d.on("click", ".link-hide-popover",
                    function(b) {
                        b.preventDefault();
                        var c = a(this).closest(".popover");
                        mcw.popover(c.data("target"), "hide")
                    }),
                    c.autohide && a(document).bind("mousedown.popover",
                    function(c) {
                        if (a(".dialog").length) return;
                        var e = a(c.target);
                        if (e[0] == b[0] || d.has(e).length) return;
                        mcw.popover(b, "hide")
                    }),
                    b.addClass("popover-target").data("popover", d),
                    d
                }
                b = a(b);
                var d = b.data("popover");
                if (d) return f(b, d),
                d
            }
        },
        highlight: function(a, b, c) {
            c = c || "transparent",
            a.stop(!0, !0).css({
                backgroundColor: b || "#fffed6"
            }),
            setTimeout(function() {
                a.animate({
                    backgroundColor: c
                },
                {
                    queue: !1,
                    duration: 1e3
                })
            },
            100)
        },
        scrollLoad: function(b, c) {
            function g() {
                if (f.offset().top - e.scrollTop() < d) {
                    if (f.hasClass("loading")) return;
                    f.addClass("loading").text("正在加载更多...");
                    var a = c(f);
                    a && a.done(function(a) {
                        a ? (f.removeClass("loading").text("加载更多内容"), g()) : f.removeClass("loading").addClass("over").text("没有更多内容了").unbind("click")
                    })
                }
            }
            var d, e = a(window);
            if (b === !1) {
                a(window).unbind(".scrollLoad"),
                e.unbind(".scrollLoad");
                return
            }
            var f = a("#btn-load-more", b);
            if (!f.length) return;
            a(window).unbind(".scrollLoad").bind("resize.scrollLoad",
            function(b) {
                d = a(window).height()
            }).resize(),
            e.unbind(".scrollLoad").bind("scroll.scrollLoad",
            function(a) {
                if (f.is(".loading, .over")) return;
                g()
            }).scroll()
        },
        metaKey: function(a) {
            var b = /Mac/.test(navigator.userAgent);
            return b ? a.metaKey: a.ctrlKey
        },
        playAudio: function(b, c) {
            var d = a("#audio-" + b);
            d.length || (d = a('<audio id="audio-' + b + '">\t\t\t\t\t\t<source src="' + c + '" type="audio/mpeg" />\t\t\t\t\t</audio>').appendTo("body")),
            d = d.get(0),
            a.browser.chrome && d.load(),
            d.play()
        },
        prettyDate: function(a, b) {
            var c = moment(a, b),
            d = mcw.now(),
            e = d.diff(c);
            if (e < 0) return "刚刚";
            if (c.diff(d.clone().add("d", -1).startOf("day")) < 0) return c.format("M月D日");
            if (c.diff(d.clone().startOf("day")) < 0) return "昨天";
            if (e < 6e4) return "刚刚";
            if (e >= 6e4 && e < 36e5) return Math.round(e / 6e4).toFixed(0) + "分钟前";
            if (e >= 36e5 && e < 864e5) return Math.round(e / 36e5).toFixed(0) + "小时前"
        },
        autosave: function(b) {
            b = b || document;
            var c = a("[data-autosave]", b),
            d = mcw.urlParts(location.href),
            e = [];
            c.each(function(b, c) {
                var c = a(c),
                f = c.data("autosave"),
                g = d.path + f + "/autosave/";
                if (!f) return;
                c.off("keyup.autosave").on("keyup.autosave",
                function() {
                    var b = a(this).val();
                    localStorage[g] = b
                }),
                localStorage[g] && c.val(localStorage[g]),
                e.push(g)
            }),
            c.closest(".form").off("ajax:success.autosave").on("ajax:success.autosave",
            function(b) {
                a.each(e,
                function(a, b) {
                    localStorage[b] = "",
                    localStorage.removeItem(b)
                })
            })
        },
        isScreenView: function(b, c, d) {
            b = a(b),
            c = c || 0;
            var e = b.offset(),
            f = a(window),
            g = a(document),
            h = !1;
            return ! d && e.top > g.scrollTop() + c && e.top < g.scrollTop() + f.height() - b.outerHeight() - c && (h = !0),
            d && (e.top > g.scrollTop() + c && e.top < g.scrollTop() + f.height() - c || e.top + b.outerHeight() > g.scrollTop() + c && e.top + b.outerHeight() < g.scrollTop() + f.height() - c) && (h = !0),
            h
        },
        templateDueFormat: function(a) {
            if (!a) return "";
            var b = a.split(","),
            c = /^\d+$/,
            d = ["日", "一", "二", "三", "四", "五", "六"];
            return b.length !== 2 || !c.test(b[0]) || !c.test(b[1]) ? "": "第" + b[0] + "周周" + d[b[1] * 1]
        }
    }
} (jQuery),
function(a) {
    a(function() {
        //mcw.
        //preloadImages(["/static/classic/images/blank-3dbe121a376a181f0fe840fb1daeeb51.gif", "/static/classic/images/loading-665030080668b5e043705395c74dc61a.gif", "/static/classic/images/icon-enter-key-85ea1f3d6deb90d9a48d4cdc5e34298a.png", "/static/classic/images/back-to-top-aa485503b416e67b699c82ee4f7638d0.png", "/static/classic/images/tiny-loading-e8bd9af828c29751e76f3d73d4f9e005.gif", "/static/classic/images/todo-actions-icon-03198277d00fa322f26853a9fcac697a.png", "/static/classic/images/todo-actions-icon-today-a8bd827d9d61e3a2d8d06303e631d79c.png", "/static/classic/images/popover-arrow-eb2c165f449ad2547233a5fdffc20730.png", "/static/classic/images/popover-arrow-gray-57a0cf7ea84aa3cff6ef5954f2d5145c.png"]),
        a.browser.msie && a.browser.version.indexOf(10) === 0 && a("body").addClass("ie10"),
        a(document).on("click", "#link-feedback", mcw.feedbackClick).on("click", "#dialog-feedback .twr-show-feedback",
        function(b) {
            a(this).closest(".twr-help-topics").hide(100),
            a(this).closest("#dialog-feedback").find("form").show(100),
            a(this).closest("#dialog-feedback").find("textarea").focus()
        }).on("click", "*[data-origin-src]",
        function(b) {
            var c = a(this),
            d = mcw.metaKey(b);
            d ? window.open(c.attr("data-origin-src")) : mcw.viewImage(c)
        }).on("mouseenter", "*[tooltip]",
        function(b) {
            var c = a(b.currentTarget),
            d = c.attr("tooltip");
            mcw.tooltip(c, d)
        }).on("mouseleave", "*[tooltip]",
        function(b) {
            var c = a(b.currentTarget);
            mcw.tooltip(c, "hide")
        }).on("beforestack",
        function(b) {
            a("*[tooltip]").trigger("mouseleave"),
            mcw.popover("clear"),
            a(document).trigger("mousedown.notipop");
            var c = !0;
            a(".mcw-editor").each(function(b, d) {
                var e = a(d).closest(".form");
                if (e.find(".attachment.uploading:visible").length && !window.confirm("有文件正在上传中，离开当前页将会自动放弃上传，确定要离开？")) {
                    c = !1;
                    return
                }
                e.find(".btn-cancel-update-comment, .btn-cancel-create-comment, #link-cancel-post").click()
            });
            if (!c) return c;
            mcw.scrollLoad(!1),
            a(".header .nav li.active").removeClass("active")
        }).on("afterstack",
        function(a, b) {
            mcw.adjustDate(b),
            mcw.adjustPermission(b)
        }).on("click", ".noti-pop .noti-pop-list .notice .link",
        function(b) {
            var c = a(this).closest(".notice").data("notification-guid");
            mcw.readNotification(c)
        }).on("click", ".back-to-top",
        function(a) {
            a.preventDefault(),
            mcw.scrollTo("body")
        }).on("ajax:success", ".detail-action-star",
        function(b) {
            b.preventDefault();
            var c = a(b.target);
            c.hasClass("stared") ? c.removeClass("stared").text("加星标").attr("title", "加星标") : c.addClass("stared").text("取消星标").attr("title", "取消星标")
        }).on("ajax:success", ".star-action",
        function(b) {
            b.preventDefault();
            var c = a(b.target).parent(".minicard");
            c.fadeOut("fast",
            function() {
                this.remove()
            })
        }).on("click", ".detail-action-move .detail-action",
        function(b) {
            b.preventDefault();
            var c = a(b.target),
            d = c.next(".confirm"),
            e = d.find(".choose-projects"),
            f = d.find("button[type=submit]"),
            g = d.closest(".item");
            g.addClass("expanded");
            if (!e.is(".loading")) return;
            a.ajax({
                url: "/members/" + mcw.me.guid + "/projects/",
                type: "get",
                dataType: "json",
                success: function(b) {
                    var c = "",
                    d = e.data("project");
                    if (b.length === 1 && b[0].guid === d) {
                        e.find("option").text("没有可选项目...");
                        return
                    }
                    a.each(b,
                    function(a, b) {
                        d !== b.guid && (c += '<option value="' + b.guid + '">' + mcw.encodeHtml(b.name) + "</option>")
                    }),
                    e.html(c).prop("disabled", !1).removeClass("loading"),
                    f.prop("disabled", !1)
                }
            })
        }).on("click", ".detail-actions .confirm .cancel",
        function(b) {
            b.preventDefault();
            var c = a(b.target);
            c.closest(".item").removeClass("expanded")
        }).on("ajax:beforeSend", ".form-move",
        function(b, c, d) {
            a(this).find(".cancel").hide()
        }).on("ajax:complete", ".form-move",
        function() {
            a(this).find(".cancel").show()
        }).on("ajax:success", ".form-move",
        function(b, c) {
            if (c.success) {
                var d = a(this),
                e = d.closest(".detail-actions"),
                f = e.closest(".page"),
                g = a('<div class="mask hide"></div>'),
                h = a('<div class="moved hide"><div class="inr">移动完成，这个条目已被移到 <em>' + c.proj_name + '</em> 中，<a data-nocache data-stack data-stack-root data-parent-name="' + c.proj_name + '" data-parent-url="' + c.proj_url + '" href="' + c.url + '">现在就去查看 →</a></div></div>');
                e.fadeOut("fast",
                function() {
                    e.remove()
                }),
                g.appendTo(f).fadeIn(function() {
                    h.appendTo(f).slideDown()
                })
            }
        }).on("click", ".btn-radios .btn",
        function(b) {
            var c = a(b.currentTarget);
            c.siblings(".btn.active").removeClass("active").end().addClass("active")
        }).on("click", ".link-member-menu",
        function(b) {
            var c = a(b.currentTarget),
            d = mcw.template("tpl-member-menu");
            mcw.popover(c, {
                content: d,
                position: "bottom-left",
                cls: "popover-member-menu",
                offset: {
                    top: 5,
                    left: 0
                }
            })
        }).on("validate", ".form-editor",
        function(b, c, d) {
            var e = a(this).find(".mcw-editor:first"),
            f = e.find(".attachment:visible"),
            g = a(b.currentTarget),
            h = {
                valid: !0
            };
            return ! c.replace(/<[^>]+>/ig, "") && !a.trim(g.find("input[type=text]").val()) && !f.length ? (e.addClass("error"), h.valid = !1) : e.removeClass("error"),
            f.each(function() {
                if (a(this).hasClass("uploading")) return e.addClass("error"),
                h.valid = !1,
                !1
            }),
            h
        }).on("ajax:beforeSend", ".form-editor",
        function(b, c, d) {
            var e = a(".member-list input:checked").map(function() {
                return a(this).val()
            }).get();
            d.data += "&cc_guids=" + e.join(",");
            var f = a(this).find(".mcw-editor:first"),
            g = f.find(".attachment[fileid]:visible").map(function() {
                return a(this).is("[attachId]") ? a(this).attr("attachId") : null
            }).get(),
            h = f.find(".attachment:hidden:not([fileid])").map(function() {
                return a(this).is("[attachId]") ? a(this).attr("attachId") : null
            }).get(),
            i = f.find(".attachment:visible").map(function() {
                return a(this).is("[attachId]") ? a(this).attr("attachId") : null
            }).get();
            d.data += "&attach_guids=" + g.join(",") + "&delete_attach_guids=" + h.join(",") + "&attach_order=" + i.join(",")
        }).on("click", ".link-select-all",
        function(b) {
            b.preventDefault(),
            a(b.currentTarget).parents(".notify:first").find(".member-list input:checkbox").attr("checked", "checked")
        }).on("click", ".link-select-none",
        function(b) {
            b.preventDefault(),
            a(b.currentTarget).parents(".notify:first").find(".member-list input:checkbox").removeAttr("checked")
        }).on("click", ".link-change-notify",
        function(b) {
            b.preventDefault(),
            a(b.currentTarget).parent().hide().parents(".notify:first").find(".select-all").show().end().find(".form-field").show().end().find(".receiver").hide()
        }),
        function() {
            var b = 0,
            c = null,
            d = a(document);
            a(window).bind("resize.backTop",
            function(c) {
                b = a(this).height()
            }).resize(),
            d.bind("scroll.backTop",
            function(e) {
                d.scrollTop() > b * 1.5 ? c || (c = a('<a class="back-to-top" href="#" title="返回顶部">返回顶部</a>').appendTo(".page:last")) : c && (c.remove(), c = null)
            })
        } (),
        a("#notification-count").on("mousedown",
        function() {
            var b = a(".noti-pop");
            return b.hasClass("on") ? a(document).trigger("mousedown.notipop") : (b.addClass("on"), a(document).unbind(".notipop").bind("mousedown.notipop",
            function(c) {
                var d = a(c.target);
                d.closest(".noti-pop").length || (b.removeClass("on"), a(document).unbind(".notipop"))
            })),
            !1
        }),
        a("#noti-mark-read").click(function(b) {
            b.preventDefault(),
            a("#notification-count").text(0).removeClass("unread"),
            a(".noti-pop-list").empty().hide(),
            a(".noti-pop-empty").show(),
            a(document).trigger("mousedown.notipop"),
            a.ajax({
                url: "/notifications/read_all/"
            })
        }),
        a(".search-wrap").on("click",
        function(a) {
            return ! 1
        }).on("click", ".link-search",
        function(b) {
            var c = a(b.currentTarget).closest(".search-wrap"),
            d = a(document),
            e = a("#form-search");
            if (c.hasClass("active")) return;
            return c.addClass("active").find("#txt-search").focus(),
            d.one("click.search",
            function(a) {
                c.removeClass("active").find("#txt-search").val(""),
                d.unbind("keyup.search")
            }).bind("keyup.search",
            function(a) {
                a.keyCode == 27 && (a.preventDefault(), d.trigger("click.search"))
            }),
            !1
        }),
        a("#txt-search").bind("keyup DOMAutoComplete",
        function() {
            a.trim(a(this).val()).length ? a(this).addClass("enter") : a(this).removeClass("enter")
        }).on("keydown",
        function(b) {
            var c = a(this);
            if (b.which == 13) {
                var d = a.trim(c.val());
                return d ? (a("#page-search-result").empty().addClass("loading"), mcw.stack({
                    url: a("#form-search").attr("action") + "?keyword=" + encodeURIComponent(d),
                    root: !0
                }), c.val(d).get(0).select()) : c.val(""),
                !1
            }
        }).on("focus",
        function(b) {
            var c = a(b.currentTarget).closest(".search-wrap"),
            d = a(document),
            e = a("#form-search");
            if (c.hasClass("active")) return;
            return c.addClass("active"),
            d.one("click.search",
            function(a) {
                c.removeClass("active").find("#txt-search").val(""),
                d.unbind("keyup.search")
            }).bind("keyup.search",
            function(a) {
                a.keyCode == 27 && (a.preventDefault(), d.trigger("click.search"))
            }),
            !1
        }),
        a.fn.placeholder && a("input[placeholder], textarea[placeholder]").placeholder(),
        mcw.me = {
            guid: a("#member-guid").val(),
            nickname: a("#member-nickname").val(),
            avatar: a("#member-avatar").val(),
            admin: a("#member-admin").length > 0 ? !0 : !1,
            owner: a("#member-owner").length > 0 ? !0 : !1
        };
        var b = a(".workspace .page:last"),
        c = b.attr("id");
        c && mcw.pages[c] && mcw.pages[c].init(b),
        mcw.me.guid && mcw.live(),
        mcw.me.avatar && mcw.preloadImages([mcw.me.avatar]),
        mcw.adjustDate(b),
        mcw.adjustPermission(b),
        setInterval(function() {
            mcw.adjustDate()
        },
        6e4)
    }),
    a.browser.webkit && a(window).on("load",
    function() {
        var b = a(":focus");
        b.length && b.is("input, textarea") && mcw.selectText(b[0])
    }),
    a.extend(window.mcw, {
        pages: {},
        members: {},
        feedbackClick: function(b) {
            b.preventDefault();
            var c = mcw.dialog({
                el: mcw.template("tpl-feedback")
            });
            a("#dialog-feedback input[name=page_url]").val(location.href),
            c.find("#txt-feedback").focus(),
            c.find("#link-cancel-feedback").click(function(a) {
                a.preventDefault(),
                mcw.dialog("hide")
            }),
            c.find("form.form-feedback").on("ajax:success",
            function(a) {
                mcw.message({
                    msg: "感谢你的反馈，我们将会在 1 个工作日内回复"
                })
            }),
            mcw.fetchHelpTopics(c)
        },
        fetchHelpTopics: function(b) {
            b.find("form").hide(),
            b.find(".twr-help-topics").hide(),
            a.get("/help_topics/by_context",
            function(c) {
                var d = b.find("ul");
                d.empty(),
                c.length ? (a.each(c,
                function(a, b) {
                    d.append('<li><i class="icon-question-sign"></i><a href="' + b.url + '" target="_blank">' + b.subject + "</a></li>")
                }), b.find(".twr-help-topics").show()) : b.find("form").show()
            })
        },
        d18n: {
            support: function() {
                return a.browser.safari ? !!window.Notification: a.browser.chrome ? !!window.webkitNotifications: !1
            },
            permitted: function() {
                if (!mcw.d18n.support()) return ! 1;
                if (a.browser.safari) return "granted" === Notification.permission || a.isFunction(Notification.permissionLevel) && Notification.permissionLevel();
                if (a.browser.chrome) return webkitNotifications.checkPermission() == 0
            },
            requestPermission: function(b) {
                if (!mcw.d18n.support()) return;
                b = b ||
                function() {},
                a.browser.safari ? Notification.requestPermission(b) : a.browser.chrome && webkitNotifications.requestPermission(b)
            },
            show: function(b) {
                if (!mcw.d18n.support()) return;
                var c = null;
                a.browser.safari ? c = new Notification(b.title, b.content) : a.browser.chrome && (c = webkitNotifications.createNotification("/static/classic/images/icon-tower-479344ffcf99c7852fa40955302e15ac.png", b.title, b.content)),
                c.onclick = function() {
                    mcw.stack({
                        url: b.url,
                        root: !0,
                        parent: {
                            name: "全部通知",
                            url: "/teams/" + b.team + "/notifications/"
                        }
                    }),
                    mcw.readNotification(b.guid),
                    window.focus(),
                    this.cancel()
                },
                mcw.playAudio("notification", "/static/classic/images/notification-cc3cfeed3b317b42296450911fae479a.mp3"),
                c.show(),
                setTimeout(function() {
                    c && c.cancel()
                },
                1e4)
            }
        },
        metaKey: function(a) {
            var b = /Mac/.test(navigator.userAgent);
            return b ? a.metaKey: a.ctrlKey
        },
        readNotification: function(b) {
            var c = a("#notification-count"),
            d = Math.max(0, c.text() * 1 - 1);
            c.toggleClass("unread", d > 0).text(d);
            var e = a(".noti-pop-list");
            e.find(".notice[data-notification-guid=" + b + "]").remove(),
            e.find(".notice").length || (e.html("").hide(), a(".noti-pop-empty").show())
        },
        adjustDate: function(b) {
            a("[data-abstime]", b).each(function() {
                var b = a(this);
                b.text(mcw.prettyDate(b.data("abstime"), "YYYY-MM-DD HH:mm:ss Z"))
            })
        },
        adjustPermission: function(b) {
            b = a(b).is("[data-visible-to]") ? a(b) : a("[data-visible-to]", b),
            b.each(function() {
                var b = a(this).hide(),
                c = b.data("visible-to").split(",");
                mcw.me.admin && a.inArray("admin", c) > -1 && b.show();
                if (a.inArray("creator", c) > -1) {
                    var d = b.closest("[data-author-guid]");
                    d.length && mcw.me.guid == d.data("author-guid") && b.show()
                }
            })
        },
        adjustProjInfo: function() {
            var b = a(".workspace .page:last .project-info"),
            c = a(".workspace .sheet-header .link-parent-sheet");
            c.each(function() {
                var c = a(this).text(),
                d = b.find("a:contains(" + c + ")");
                d.length && d.closest("span").remove()
            }),
            b.find("span").length || b.remove()
        },
        adjustStar: function() {
            var b = a(".detail-action-star"),
            c = b.data("itemtype"),
            d = b.data("itemid");
            if (!b.length || !c || !d) return;
            a.ajax({
                url: "/members/" + mcw.me.guid + "/has_star/",
                type: "get",
                data: {
                    starable_type: c,
                    starable_id: d
                },
                success: function(a) {
                    a.has_star && b.addClass("stared").text("取消星标").attr("title", "取消星标")
                }
            })
        }
    });
    if (a.ui && a.ui.sortable) {
        var b = a.ui.sortable.prototype._mouseStart;
        a.ui.sortable.prototype._mouseStart = function(a, c, d) {
            this._trigger("beforestart", a, this._uiHash()),
            b.apply(this, [a, c, d])
        };
        var c = a.fn.scrollParent;
        a.fn.scrollParent = function() {
            var b = c.apply(this, arguments);
            return b.is("html") ? a(document) : b
        }
    }
    if (a.ui && a.ui.draggable) {
        var d = a.ui.draggable.prototype._mouseStart;
        a.ui.draggable.prototype._mouseStart = function(a, b, c) {
            this._trigger("beforestart", a, this._uiHash()),
            d.apply(this, [a, b, c])
        }
    }
} (jQuery),
function(a) {
    function d(c) {
        var d = a("#player li").stop(!0, !0),
        e = a("#ctrl li");
        newIndex = isNaN(c) ? b + 1 : c,
        newSlide = d.eq(newIndex),
        newSlide.length || (newSlide = d.eq(0), newIndex = 0),
        d.eq(b).fadeOut(100),
        newSlide.fadeIn(100,
        function() {
            a(this).addClass("cur").siblings("li").removeClass("cur")
        }),
        e.removeClass("cur").eq(newIndex).addClass("cur"),
        b = newIndex
    }
    a(function() {
        function b(a) {
            return Math.floor(Math.random() * a + 1)
        }
        a("#cloud-hl").addClass("bg" + b(4)),
        a(".cloud-form").on("ajax:success", "form",
        function(b) {
            a(this).find(".suc").show(),
            a(this).find(".btn-submit").hide()
        }),
        a(".video-preview").click(function(b) {
            b.preventDefault();
            var c = a(this),
            d = c.offset(),
            e = parseInt(c.css("border-top-width")),
            f = parseInt(c.css("border-left-width")),
            g = {
                width: c.width(),
                height: c.height(),
                top: d.top - a(document).scrollTop() + e,
                left: d.left - a(document).scrollLeft() + f
            },
            h = a("<div id='mask' class='hidden'></div>").appendTo("body"),
            i = a("<div class='video'></div>").css({
                width: g.width,
                height: g.height,
                top: g.top,
                left: g.left
            }).appendTo("body"),
            j = null,
            k = null;
            c.find(".btn-play").hide(),
            a("<img/>").attr({
                src: c.find("img").attr("src")
            }).appendTo(i);
            var l = function() {
                k && (k.pause(), k.destroy(), k = null),
                setTimeout(function() {
                    i.find("#video").remove(),
                    i.append(j),
                    mcw.transitionEnd(h,
                    function() {
                        h.remove()
                    }),
                    mcw.transitionEnd(i,
                    function() {
                        i.remove(),
                        c.find(".btn-play").show()
                    }),
                    d = c.offset(),
                    g.top = d.top - a(document).scrollTop() + e,
                    g.left = d.left - a(document).scrollLeft() + f,
                    h.addClass("hidden"),
                    i.css({
                        width: g.width,
                        height: g.height,
                        top: g.top,
                        left: g.left
                    })
                },
                50)
            };
            h.click(function(a) {
                l()
            }),
            setTimeout(function() {
                var b = c.data("video-width"),
                d = c.data("video-height");
                mcw.transitionEnd(i,
                function() {
                    j = i.find("img").remove(),
                    i.html('<video id="video" class="video-js vjs-default-skin" width="' + b + '" height="' + d + '" controls poster="/static/classic/images/video-preview-431bdceb1b043aa2f98a22b989b88cc4.png" preload="auto">\t\t\t\t\t<source type="video/mp4" src="http://localhost:8000/static/classic/flash/intro.mp4">\t\t\t\t\t<source type="video/webm" src="http://localhost:8000/static/classic/flash/intro.webm">\t\t\t\t</video>\t\t\t\t<a id="close" href="javascript:;" title="关闭视频">关闭</a>'),
                    a("#close").click(function() {
                        l()
                    }),
                    setTimeout(function() {
                        k = _V_("video", {
                            flash: {
                                swf: "/static/classic/images/video-js-6e518d1400bea4ce1a96767e3d705b88.swf"
                            }
                        },
                        function() {
                            this.play()
                        })
                    },
                    0)
                }),
                i.css({
                    width: b,
                    height: d,
                    top: (a(window).height() - d) / 2,
                    left: (a(window).width() - b) / 2
                }),
                h.removeClass("hidden")
            },
            0)
        }),
        a(".apply-test").on("click",
        function(a) {
            a.preventDefault();
            var b = mcw.dialog({
                width: 500,
                el: mcw.template("tpl-apply-test")
            });
            b.find("#link-cancel-apply").click(function(a) {
                a.preventDefault(),
                mcw.dialog("hide")
            }),
            b.find("form.form-apply-test").on("ajax:success",
            function(a) {
                mcw.message({
                    msg: "感谢您的申请，我们会尽快与您联系"
                })
            })
        })
    });
    var b = 0,
    c = 1e4;
    a(function() {
        var e = setInterval(function() {
            d()
        },
        c);
        a("#ctrl li").click(function() {
            var f = a("#ctrl li"),
            g = f.index(this);
            clearInterval(e),
            e = setInterval(function() {
                d()
            },
            c),
            g != b && d(g)
        })
    })
} (jQuery)