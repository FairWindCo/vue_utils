this.primevue = this.primevue || {};
this.primevue.breadcrumb = (function (vue) {
    'use strict';

    var script = {
        name: 'BreadcrumbItem',
        props: {
            item: null,
            template: null
        },
        methods: {
            onClick(event, navigate) {
                if (this.item.command) {
                    this.item.command({
                        originalEvent: event,
                        item: this.item
                    });
                }

                if (this.item.to && navigate) {
                    navigate(event);
                }
            },
            visible() {
                return (typeof this.item.visible === 'function' ? this.item.visible() : this.item.visible !== false);
            }
        },
        computed: {
            containerClass() {
                return [{'p-disabled': this.item.disabled}, this.item.class];
            },
            iconClass() {
                return ['p-menuitem-icon', this.item.icon];
            }
        }
    };

    const _hoisted_1 = {
      key: 1,
      class: "p-menuitem-text"
    };
    const _hoisted_2 = {
      key: 1,
      class: "p-menuitem-text"
    };

    function render(_ctx, _cache, $props, $setup, $data, $options) {
      const _component_router_link = vue.resolveComponent("router-link");

      return ($options.visible())
        ? (vue.openBlock(), vue.createBlock("li", {
            key: 0,
            class: $options.containerClass
          }, [
            (!$props.template)
              ? (vue.openBlock(), vue.createBlock(vue.Fragment, { key: 0 }, [
                  ($props.item.to)
                    ? (vue.openBlock(), vue.createBlock(_component_router_link, {
                        key: 0,
                        to: $props.item.to,
                        custom: ""
                      }, {
                        default: vue.withCtx(({navigate, href}) => [
                          vue.createVNode("a", {
                            href: href,
                            class: "p-menuitem-link",
                            onClick: $event => ($options.onClick($event, navigate))
                          }, [
                            ($props.item.icon)
                              ? (vue.openBlock(), vue.createBlock("span", {
                                  key: 0,
                                  class: $options.iconClass
                                }, null, 2))
                              : vue.createCommentVNode("", true),
                            ($props.item.label)
                              ? (vue.openBlock(), vue.createBlock("span", _hoisted_1, vue.toDisplayString($props.item.label), 1))
                              : vue.createCommentVNode("", true)
                          ], 8, ["href", "onClick"])
                        ]),
                        _: 1
                      }, 8, ["to"]))
                    : (vue.openBlock(), vue.createBlock("a", {
                        key: 1,
                        href: $props.item.url||'#',
                        class: "p-menuitem-link",
                        onClick: _cache[1] || (_cache[1] = (...args) => ($options.onClick && $options.onClick(...args))),
                        target: $props.item.target
                      }, [
                        ($props.item.icon)
                          ? (vue.openBlock(), vue.createBlock("span", {
                              key: 0,
                              class: $options.iconClass
                            }, null, 2))
                          : vue.createCommentVNode("", true),
                        ($props.item.label)
                          ? (vue.openBlock(), vue.createBlock("span", _hoisted_2, vue.toDisplayString($props.item.label), 1))
                          : vue.createCommentVNode("", true)
                      ], 8, ["href", "target"]))
                ], 64))
              : (vue.openBlock(), vue.createBlock(vue.resolveDynamicComponent($props.template), {
                  key: 1,
                  item: $props.item
                }, null, 8, ["item"]))
          ], 2))
        : vue.createCommentVNode("", true)
    }

    script.render = render;

    var script$1 = {
        name: 'Breadcrumb',
        props: {
            model: {
                type: Array,
                default: null
            },
            home: {
                type: null,
                default: null
            }
        },
        components: {
            'BreadcrumbItem': script
        }
    };

    const _hoisted_1$1 = {
      class: "p-breadcrumb p-component",
      "aria-label": "Breadcrumb"
    };
    const _hoisted_2$1 = /*#__PURE__*/vue.createVNode("li", { class: "p-breadcrumb-chevron pi pi-chevron-right" }, null, -1);

    function render$1(_ctx, _cache, $props, $setup, $data, $options) {
      const _component_BreadcrumbItem = vue.resolveComponent("BreadcrumbItem");

      return (vue.openBlock(), vue.createBlock("nav", _hoisted_1$1, [
        vue.createVNode("ul", null, [
          ($props.home)
            ? (vue.openBlock(), vue.createBlock(_component_BreadcrumbItem, {
                key: 0,
                item: $props.home,
                class: "p-breadcrumb-home",
                template: _ctx.$slots.item
              }, null, 8, ["item", "template"]))
            : vue.createCommentVNode("", true),
          (vue.openBlock(true), vue.createBlock(vue.Fragment, null, vue.renderList($props.model, (item) => {
            return (vue.openBlock(), vue.createBlock(vue.Fragment, {
              key: item.label
            }, [
              _hoisted_2$1,
              vue.createVNode(_component_BreadcrumbItem, {
                item: item,
                template: _ctx.$slots.item
              }, null, 8, ["item", "template"])
            ], 64))
          }), 128))
        ])
      ]))
    }

    function styleInject(css, ref) {
      if ( ref === void 0 ) ref = {};
      var insertAt = ref.insertAt;

      if (!css || typeof document === 'undefined') { return; }

      var head = document.head || document.getElementsByTagName('head')[0];
      var style = document.createElement('style');
      style.type = 'text/css';

      if (insertAt === 'top') {
        if (head.firstChild) {
          head.insertBefore(style, head.firstChild);
        } else {
          head.appendChild(style);
        }
      } else {
        head.appendChild(style);
      }

      if (style.styleSheet) {
        style.styleSheet.cssText = css;
      } else {
        style.appendChild(document.createTextNode(css));
      }
    }

    var css_248z = "\n.p-breadcrumb ul {\n    margin: 0;\n    padding: 0;\n    list-style-type: none;\n    display: -webkit-box;\n    display: -ms-flexbox;\n    display: flex;\n    -webkit-box-align: center;\n        -ms-flex-align: center;\n            align-items: center;\n    -ms-flex-wrap: wrap;\n        flex-wrap: wrap;\n}\n.p-breadcrumb .p-menuitem-text {\n    line-height: 1;\n}\n.p-breadcrumb .p-menuitem-link {\n    text-decoration: none;\n}\n";
    styleInject(css_248z);

    script$1.render = render$1;

    return script$1;

}(Vue));
