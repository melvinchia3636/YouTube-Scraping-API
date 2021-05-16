/*! For license information please see theme.js.LICENSE.txt */ ! function() {
    var t = {
		152: function(t) {
			var e;
			e = function() {
				return function() {
					var t = {
							134: function(t, e, n) {
								"use strict";
								n.d(e, {
									default: function() {
										return b
									}
								});
								var r = n(279),
									o = n.n(r),
									i = n(370),
									c = n.n(i),
									a = n(817),
									u = n.n(a);

								function l(t) {
									return (l = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
										return typeof t
									} : function(t) {
										return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
									})(t)
								}

								function s(t, e) {
									for (var n = 0; n < e.length; n++) {
										var r = e[n];
										r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
									}
								}
								var f = function() {
									function t(e) {
										! function(t, e) {
											if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
										}(this, t), this.resolveOptions(e), this.initSelection()
									}
									var e, n;
									return e = t, (n = [{
										key: "resolveOptions",
										value: function() {
											var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
											this.action = t.action, this.container = t.container, this.emitter = t.emitter, this.target = t.target, this.text = t.text, this.trigger = t.trigger, this.selectedText = ""
										}
									}, {
										key: "initSelection",
										value: function() {
											this.text ? this.selectFake() : this.target && this.selectTarget()
										}
									}, {
										key: "createFakeElement",
										value: function() {
											var t = "rtl" === document.documentElement.getAttribute("dir");
											this.fakeElem = document.createElement("textarea"), this.fakeElem.style.fontSize = "12pt", this.fakeElem.style.border = "0", this.fakeElem.style.padding = "0", this.fakeElem.style.margin = "0", this.fakeElem.style.position = "absolute", this.fakeElem.style[t ? "right" : "left"] = "-9999px";
											var e = window.pageYOffset || document.documentElement.scrollTop;
											return this.fakeElem.style.top = "".concat(e, "px"), this.fakeElem.setAttribute("readonly", ""), this.fakeElem.value = this.text, this.fakeElem
										}
									}, {
										key: "selectFake",
										value: function() {
											var t = this,
												e = this.createFakeElement();
											this.fakeHandlerCallback = function() {
												return t.removeFake()
											}, this.fakeHandler = this.container.addEventListener("click", this.fakeHandlerCallback) || !0, this.container.appendChild(e), this.selectedText = u()(e), this.copyText(), this.removeFake()
										}
									}, {
										key: "removeFake",
										value: function() {
											this.fakeHandler && (this.container.removeEventListener("click", this.fakeHandlerCallback), this.fakeHandler = null, this.fakeHandlerCallback = null), this.fakeElem && (this.container.removeChild(this.fakeElem), this.fakeElem = null)
										}
									}, {
										key: "selectTarget",
										value: function() {
											this.selectedText = u()(this.target), this.copyText()
										}
									}, {
										key: "copyText",
										value: function() {
											var t;
											try {
												t = document.execCommand(this.action)
											} catch (e) {
												t = !1
											}
											this.handleResult(t)
										}
									}, {
										key: "handleResult",
										value: function(t) {
											this.emitter.emit(t ? "success" : "error", {
												action: this.action,
												text: this.selectedText,
												trigger: this.trigger,
												clearSelection: this.clearSelection.bind(this)
											})
										}
									}, {
										key: "clearSelection",
										value: function() {
											this.trigger && this.trigger.focus(), document.activeElement.blur(), window.getSelection().removeAllRanges()
										}
									}, {
										key: "destroy",
										value: function() {
											this.removeFake()
										}
									}, {
										key: "action",
										set: function() {
											var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "copy";
											if (this._action = t, "copy" !== this._action && "cut" !== this._action) throw new Error('Invalid "action" value, use either "copy" or "cut"')
										},
										get: function() {
											return this._action
										}
									}, {
										key: "target",
										set: function(t) {
											if (void 0 !== t) {
												if (!t || "object" !== l(t) || 1 !== t.nodeType) throw new Error('Invalid "target" value, use a valid Element');
												if ("copy" === this.action && t.hasAttribute("disabled")) throw new Error('Invalid "target" attribute. Please use "readonly" instead of "disabled" attribute');
												if ("cut" === this.action && (t.hasAttribute("readonly") || t.hasAttribute("disabled"))) throw new Error('Invalid "target" attribute. You can\'t cut text from elements with "readonly" or "disabled" attributes');
												this._target = t
											}
										},
										get: function() {
											return this._target
										}
									}]) && s(e.prototype, n), t
								}();

								function d(t) {
									return (d = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
										return typeof t
									} : function(t) {
										return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
									})(t)
								}

								function h(t, e) {
									for (var n = 0; n < e.length; n++) {
										var r = e[n];
										r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
									}
								}

								function p(t, e) {
									return (p = Object.setPrototypeOf || function(t, e) {
										return t.__proto__ = e, t
									})(t, e)
								}

								function y(t, e) {
									return !e || "object" !== d(e) && "function" != typeof e ? function(t) {
										if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
										return t
									}(t) : e
								}

								function m(t) {
									return (m = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
										return t.__proto__ || Object.getPrototypeOf(t)
									})(t)
								}

								function v(t, e) {
									var n = "data-clipboard-".concat(t);
									if (e.hasAttribute(n)) return e.getAttribute(n)
								}
								var b = function(t) {
									! function(t, e) {
										if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
										t.prototype = Object.create(e && e.prototype, {
											constructor: {
												value: t,
												writable: !0,
												configurable: !0
											}
										}), e && p(t, e)
									}(u, t);
									var e, n, r, o, i, a = (o = u, i = function() {
										if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
										if (Reflect.construct.sham) return !1;
										if ("function" == typeof Proxy) return !0;
										try {
											return Date.prototype.toString.call(Reflect.construct(Date, [], (function() {}))), !0
										} catch (t) {
											return !1
										}
									}(), function() {
										var t, e = m(o);
										if (i) {
											var n = m(this).constructor;
											t = Reflect.construct(e, arguments, n)
										} else t = e.apply(this, arguments);
										return y(this, t)
									});

									function u(t, e) {
										var n;
										return function(t, e) {
											if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
										}(this, u), (n = a.call(this)).resolveOptions(e), n.listenClick(t), n
									}
									return e = u, r = [{
										key: "isSupported",
										value: function() {
											var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : ["copy", "cut"],
												e = "string" == typeof t ? [t] : t,
												n = !!document.queryCommandSupported;
											return e.forEach((function(t) {
												n = n && !!document.queryCommandSupported(t)
											})), n
										}
									}], (n = [{
										key: "resolveOptions",
										value: function() {
											var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
											this.action = "function" == typeof t.action ? t.action : this.defaultAction, this.target = "function" == typeof t.target ? t.target : this.defaultTarget, this.text = "function" == typeof t.text ? t.text : this.defaultText, this.container = "object" === d(t.container) ? t.container : document.body
										}
									}, {
										key: "listenClick",
										value: function(t) {
											var e = this;
											this.listener = c()(t, "click", (function(t) {
												return e.onClick(t)
											}))
										}
									}, {
										key: "onClick",
										value: function(t) {
											var e = t.delegateTarget || t.currentTarget;
											this.clipboardAction && (this.clipboardAction = null), this.clipboardAction = new f({
												action: this.action(e),
												target: this.target(e),
												text: this.text(e),
												container: this.container,
												trigger: e,
												emitter: this
											})
										}
									}, {
										key: "defaultAction",
										value: function(t) {
											return v("action", t)
										}
									}, {
										key: "defaultTarget",
										value: function(t) {
											var e = v("target", t);
											if (e) return document.querySelector(e)
										}
									}, {
										key: "defaultText",
										value: function(t) {
											return v("text", t)
										}
									}, {
										key: "destroy",
										value: function() {
											this.listener.destroy(), this.clipboardAction && (this.clipboardAction.destroy(), this.clipboardAction = null)
										}
									}]) && h(e.prototype, n), r && h(e, r), u
								}(o())
							},
							828: function(t) {
								if ("undefined" != typeof Element && !Element.prototype.matches) {
									var e = Element.prototype;
									e.matches = e.matchesSelector || e.mozMatchesSelector || e.msMatchesSelector || e.oMatchesSelector || e.webkitMatchesSelector
								}
								t.exports = function(t, e) {
									for (; t && 9 !== t.nodeType;) {
										if ("function" == typeof t.matches && t.matches(e)) return t;
										t = t.parentNode
									}
								}
							},
							438: function(t, e, n) {
								var r = n(828);

								function o(t, e, n, r, o) {
									var c = i.apply(this, arguments);
									return t.addEventListener(n, c, o), {
										destroy: function() {
											t.removeEventListener(n, c, o)
										}
									}
								}

								function i(t, e, n, o) {
									return function(n) {
										n.delegateTarget = r(n.target, e), n.delegateTarget && o.call(t, n)
									}
								}
								t.exports = function(t, e, n, r, i) {
									return "function" == typeof t.addEventListener ? o.apply(null, arguments) : "function" == typeof n ? o.bind(null, document).apply(null, arguments) : ("string" == typeof t && (t = document.querySelectorAll(t)), Array.prototype.map.call(t, (function(t) {
										return o(t, e, n, r, i)
									})))
								}
							},
							879: function(t, e) {
								e.node = function(t) {
									return void 0 !== t && t instanceof HTMLElement && 1 === t.nodeType
								}, e.nodeList = function(t) {
									var n = Object.prototype.toString.call(t);
									return void 0 !== t && ("[object NodeList]" === n || "[object HTMLCollection]" === n) && "length" in t && (0 === t.length || e.node(t[0]))
								}, e.string = function(t) {
									return "string" == typeof t || t instanceof String
								}, e.fn = function(t) {
									return "[object Function]" === Object.prototype.toString.call(t)
								}
							},
							370: function(t, e, n) {
								var r = n(879),
									o = n(438);
								t.exports = function(t, e, n) {
									if (!t && !e && !n) throw new Error("Missing required arguments");
									if (!r.string(e)) throw new TypeError("Second argument must be a String");
									if (!r.fn(n)) throw new TypeError("Third argument must be a Function");
									if (r.node(t)) return function(t, e, n) {
										return t.addEventListener(e, n), {
											destroy: function() {
												t.removeEventListener(e, n)
											}
										}
									}(t, e, n);
									if (r.nodeList(t)) return function(t, e, n) {
										return Array.prototype.forEach.call(t, (function(t) {
											t.addEventListener(e, n)
										})), {
											destroy: function() {
												Array.prototype.forEach.call(t, (function(t) {
													t.removeEventListener(e, n)
												}))
											}
										}
									}(t, e, n);
									if (r.string(t)) return function(t, e, n) {
										return o(document.body, t, e, n)
									}(t, e, n);
									throw new TypeError("First argument must be a String, HTMLElement, HTMLCollection, or NodeList")
								}
							},
							817: function(t) {
								t.exports = function(t) {
									var e;
									if ("SELECT" === t.nodeName) t.focus(), e = t.value;
									else if ("INPUT" === t.nodeName || "TEXTAREA" === t.nodeName) {
										var n = t.hasAttribute("readonly");
										n || t.setAttribute("readonly", ""), t.select(), t.setSelectionRange(0, t.value.length), n || t.removeAttribute("readonly"), e = t.value
									} else {
										t.hasAttribute("contenteditable") && t.focus();
										var r = window.getSelection(),
											o = document.createRange();
										o.selectNodeContents(t), r.removeAllRanges(), r.addRange(o), e = r.toString()
									}
									return e
								}
							},
							279: function(t) {
								function e() {}
								e.prototype = {
									on: function(t, e, n) {
										var r = this.e || (this.e = {});
										return (r[t] || (r[t] = [])).push({
											fn: e,
											ctx: n
										}), this
									},
									once: function(t, e, n) {
										var r = this;

										function o() {
											r.off(t, o), e.apply(n, arguments)
										}
										return o._ = e, this.on(t, o, n)
									},
									emit: function(t) {
										for (var e = [].slice.call(arguments, 1), n = ((this.e || (this.e = {}))[t] || []).slice(), r = 0, o = n.length; r < o; r++) n[r].fn.apply(n[r].ctx, e);
										return this
									},
									off: function(t, e) {
										var n = this.e || (this.e = {}),
											r = n[t],
											o = [];
										if (r && e)
											for (var i = 0, c = r.length; i < c; i++) r[i].fn !== e && r[i].fn._ !== e && o.push(r[i]);
										return o.length ? n[t] = o : delete n[t], this
									}
								}, t.exports = e, t.exports.TinyEmitter = e
							}
						},
						e = {};

					function n(r) {
						if (e[r]) return e[r].exports;
						var o = e[r] = {
							exports: {}
						};
						return t[r](o, o.exports, n), o.exports
					}
					return n.n = function(t) {
						var e = t && t.__esModule ? function() {
							return t.default
						} : function() {
							return t
						};
						return n.d(e, {
							a: e
						}), e
					}, n.d = function(t, e) {
						for (var r in e) n.o(e, r) && !n.o(t, r) && Object.defineProperty(t, r, {
							enumerable: !0,
							get: e[r]
						})
					}, n.o = function(t, e) {
						return Object.prototype.hasOwnProperty.call(t, e)
					}, n(134)
				}().default
			}, t.exports = e()
		}
	},
	e = {};

function n(r) {
	var o = e[r];
	if (void 0 !== o) return o.exports;
	var i = e[r] = {
		exports: {}
	};
	return t[r].call(i.exports, i, i.exports, n), i.exports
}
n.n = function(t) {
		var e = t && t.__esModule ? function() {
			return t.default
		} : function() {
			return t
		};
		return n.d(e, {
			a: e
		}), e
	}, n.d = function(t, e) {
		for (var r in e) n.o(e, r) && !n.o(t, r) && Object.defineProperty(t, r, {
			enumerable: !0,
			get: e[r]
		})
	}, n.o = function(t, e) {
		return Object.prototype.hasOwnProperty.call(t, e)
	},
	function() {
		"use strict";

		function t() {
			const t = document.querySelector("#snackbar");
			t.style.opacity = 0, t.style.transform = "translate(0,100%)"
		}
		var e = n(152),
			r = n.n(e);

		function o(t) {
			const e = t.trigger,
				n = e.getAttribute("aria-label");
			e.setAttribute("aria-label", "Copied!"), setTimeout((() => {
				e.setAttribute("aria-label", n)
			}), 2500)
		}

		function i(t) {
			t.classList.toggle("active");
			const e = t.querySelector("button.expand-more");
			t.classList.contains("active") ? (e.setAttribute("aria-expanded", "true"), e.setAttribute("aria-label", "Collapse this section")) : (e.setAttribute("aria-expanded", "false"), e.setAttribute("aria-label", "Expand this section"))
		}! function() {
			const t = document.querySelector('nav[role="navigation"]'),
				e = document.querySelector("body"),
				n = document.querySelector("#screen"),
				r = document.querySelector("#closeNavBtn"),
				o = document.querySelector("#openNavBtn");
			o && (o.onclick = () => {
				t.setAttribute("data-menu", "open"), e.style.overflow = "hidden", n.style.display = "initial"
			}), r && (r.onclick = () => {
				t.setAttribute("data-menu", "closed"), e.style.removeProperty("overflow"), n.style.display = "none"
			}), n.onclick = () => {
				t.setAttribute("data-menu", "closed"), e.style.removeProperty("overflow"), n.style.display = "none"
			}, document.querySelectorAll(".nav-toc li.current a").forEach((r => {
				"open" === t.getAttribute("data-menu") && (r.onclick = () => {
					t.setAttribute("data-menu", "closed"), e.style.removeProperty("overflow"), n.style.display = "none"
				})
			}))
		}(),
		function() {
			const t = document.querySelector("#search-pane"),
				e = document.querySelector("#openSearchBtn"),
				n = document.querySelector("#closeSearchBtn");
			e && (e.onclick = () => {
				t.setAttribute("data-menu", "open")
			}), n && (n.onclick = () => {
				t.setAttribute("data-menu", "closed")
			})
		}(), setTimeout((() => {
				const e = document.querySelector("#snackbar"),
					n = document.querySelectorAll(".highlighted"),
					r = document.querySelector("#search-input");
				n.length && (e.innerHTML = '<a class="tracking-wide" href="javascript:Documentation.hideSearchWords()">' + _("Clear highlighted search results") + "</a>", e.style.opacity = 1, e.style.transform = "translate(0,0)", document.querySelector("#snackbar > a").onclick = () => {
					t(), r.value = ""
				}, r.value = n[0].textContent, r.onsearch = () => {
					Documentation.hideSearchWords(), t()
				})
			}), 500),
			function() {
				const t = document.querySelector("#searchbox"),
					e = document.querySelector("#search-input");
				t.onsubmit = t => {
					e.value.length < 1 && t.preventDefault()
				}, window.addEventListener("keydown", (t => {
					"Slash" === t.code && (e.focus(), e.value = "", t.preventDefault()), "Escape" === t.code && (e.blur(), t.preventDefault())
				}))
			}(), new(r())(".headerlink", {
				text: t => t.href
			}).on("success", o), document.querySelectorAll(".headerlink").forEach((t => {
				t.onclick = t => {
					t.preventDefault()
				}
			})), new(r())("button.copy", {
				target: t => t.parentNode.nextElementSibling
			}).on("success", o), document.querySelectorAll(".expand").forEach((t => {
				t.onclick = () => {
					t.parentElement.parentElement.classList.toggle("expanded")
				}
			})), document.querySelectorAll(".nav-toc a").forEach((t => {
				t.onfocus = t => {
					document.querySelectorAll(".expand").forEach((e => {
						const n = e.parentElement.parentElement;
						n.contains(t.target) ? n.classList.add("expanded") : n.classList.contains("current") || n.classList.remove("expanded")
					}))
				}
			})),
			function() {
				let guid = () => {
					let s4 = () => {
						return Math.floor((1 + Math.random()) * 0x10000)
							.toString(16)
							.substring(1);
					}
					return 'C'+s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
				}
				let update_toc_tree = ()=>{
					$('#main-wrapper section').each(function(){
						var top_of_element = $(this).offset().top;
						var bottom_of_element = $(this).offset().top + $(this).outerHeight() - 50;
						var bottom_of_screen = $(window).scrollTop() + $(window).innerHeight();
						var top_of_screen = $(window).scrollTop();

						if ((bottom_of_screen > top_of_element) && (top_of_screen < bottom_of_element)){
							$(`.nav-toc a[href="#${$(this).attr('id')}"]`).addClass('current');
						} else {
							$(`.nav-toc a[href="#${$(this).attr('id')}"]`).removeClass('current');
						}
					})
				}
				$(document).ready(()=>{
					$('pre').addClass('highlight');
  					var scrollbar = Scrollbar.init(document.querySelector('#main-wrapper'), {
						continuousScrolling: true,
						damping: 0.05
					  });
					$('.highlight').each(function(){
						$(this).attr('hash', guid())
						Scrollbar.init(document.querySelector(`*[hash=${$(this).attr('hash')}]`));
					})
					scrollbar.addListener(update_toc_tree)
					const hash = window.location.hash;
					if (hash) {
						const target = document.getElementById(hash.substring(1));
						if (target) {
						  scrollbar.scrollIntoView(target, {
							offsetTop: -scrollbar.containerEl.scrollTop+80,
						  });
						}
					  }
					  
					  window.addEventListener('hashchange', function () {
						const hash = window.location.hash;
						if (hash) {
						  const target = document.getElementById(hash.substring(1));
						  if (target) {
							scrollbar.scrollIntoView(target, {
							  offsetTop: -scrollbar.containerEl.scrollTop,
							});
						  }
						}
					  }, false);
				})
			}(), document.querySelectorAll(".accordion").forEach((t => {
				t.onclick = t => {
					i(t.target)
				}
			})), document.querySelectorAll(".accordion .expand-more").forEach((t => {
				t.onclick = t => {
					i(t.target.parentNode)
				}
			}))
	}()
}();