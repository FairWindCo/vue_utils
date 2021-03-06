this.primevue = this.primevue || {};
this.primevue.paginator = (function (vue, Ripple, Dropdown) {
        'use strict';

        function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

        var Ripple__default = /*#__PURE__*/_interopDefaultLegacy(Ripple);
        var Dropdown__default = /*#__PURE__*/_interopDefaultLegacy(Dropdown);

        var script = {
                name: 'CurrentPageReport',
        		inheritAttrs: false,
        		props: {
        			pageCount: {
                        type: Number,
                        default: 0
                    },
                    page: {
                        type: Number,
                        default: 0
                    },
                    first: {
                        type: Number,
                        default: 0
                    },
                    rows: {
                        type: Number,
                        default: 0
                    },
                    totalRecords: {
                        type: Number,
                        default: 0
                    },
        			template: {
        				type: String,
        				default: '({currentPage} of {totalPages})'
        			}
        		},
        		computed: {
                    text() {
                        let text = this.template
                            .replace("{currentPage}", this.page + 1)
                            .replace("{totalPages}", this.pageCount)
                            .replace("{first}", this.first + 1)
                            .replace("{last}", Math.min(this.first + this.rows, this.totalRecords))
                            .replace("{rows}", this.rows)
                            .replace("{totalRecords}", this.totalRecords);

                        return text;
                    }
        		}
        	};

        const _hoisted_1 = { class: "p-paginator-current" };

        function render(_ctx, _cache, $props, $setup, $data, $options) {
          return (vue.openBlock(), vue.createBlock("span", _hoisted_1, vue.toDisplayString($options.text), 1))
        }

        script.render = render;

        var script$1 = {
            name: 'FirstPageLink',
            computed: {
                containerClass() {
                    return ['p-paginator-first p-paginator-element p-link', {
                        'p-disabled': this.$attrs.disabled
                    }];
                }
            },
            directives: {
                'ripple': Ripple__default['default']
            }
        };

        const _hoisted_1$1 = /*#__PURE__*/vue.createVNode("span", { class: "p-paginator-icon pi pi-angle-double-left" }, null, -1);

        function render$1(_ctx, _cache, $props, $setup, $data, $options) {
          const _directive_ripple = vue.resolveDirective("ripple");

          return vue.withDirectives((vue.openBlock(), vue.createBlock("button", {
            class: $options.containerClass,
            type: "button"
          }, [
            _hoisted_1$1
          ], 2)), [
            [_directive_ripple]
          ])
        }

        script$1.render = render$1;

        var script$2 = {
            name: 'LastPageLink',
            computed: {
                containerClass() {
                    return ['p-paginator-last p-paginator-element p-link', {
                        'p-disabled': this.$attrs.disabled
                    }];
                }
            },
            directives: {
                'ripple': Ripple__default['default']
            }
        };

        const _hoisted_1$2 = /*#__PURE__*/vue.createVNode("span", { class: "p-paginator-icon pi pi-angle-double-right" }, null, -1);

        function render$2(_ctx, _cache, $props, $setup, $data, $options) {
          const _directive_ripple = vue.resolveDirective("ripple");

          return vue.withDirectives((vue.openBlock(), vue.createBlock("button", {
            class: $options.containerClass,
            type: "button"
          }, [
            _hoisted_1$2
          ], 2)), [
            [_directive_ripple]
          ])
        }

        script$2.render = render$2;

        var script$3 = {
            name: 'NextPageLink',
            computed: {
                containerClass() {
                    return ['p-paginator-next p-paginator-element p-link', {
                        'p-disabled': this.$attrs.disabled
                    }];
                }
            },
            directives: {
                'ripple': Ripple__default['default']
            }
        };

        const _hoisted_1$3 = /*#__PURE__*/vue.createVNode("span", { class: "p-paginator-icon pi pi-angle-right" }, null, -1);

        function render$3(_ctx, _cache, $props, $setup, $data, $options) {
          const _directive_ripple = vue.resolveDirective("ripple");

          return vue.withDirectives((vue.openBlock(), vue.createBlock("button", {
            class: $options.containerClass,
            type: "button"
          }, [
            _hoisted_1$3
          ], 2)), [
            [_directive_ripple]
          ])
        }

        script$3.render = render$3;

        var script$4 = {
            name: 'PageLinks',
            inheritAttrs: false,
            emits: ['click'],
            props: {
                value: Array,
                page: Number
            },
            methods: {
                onPageLinkClick(event, pageLink) {
                    this.$emit('click', {
                        originalEvent: event,
                        value: pageLink
                    });
                }
            },
            directives: {
                'ripple': Ripple__default['default']
            }
        };

        const _hoisted_1$4 = { class: "p-paginator-pages" };

        function render$4(_ctx, _cache, $props, $setup, $data, $options) {
          const _directive_ripple = vue.resolveDirective("ripple");

          return (vue.openBlock(), vue.createBlock("span", _hoisted_1$4, [
            (vue.openBlock(true), vue.createBlock(vue.Fragment, null, vue.renderList($props.value, (pageLink) => {
              return vue.withDirectives((vue.openBlock(), vue.createBlock("button", {
                key: pageLink,
                class: ['p-paginator-page p-paginator-element p-link', {'p-highlight': ((pageLink - 1) === $props.page)}],
                type: "button",
                onClick: $event => ($options.onPageLinkClick($event, pageLink))
              }, [
                vue.createTextVNode(vue.toDisplayString(pageLink), 1)
              ], 10, ["onClick"])), [
                [_directive_ripple]
              ])
            }), 128))
          ]))
        }

        script$4.render = render$4;

        var script$5 = {
            name: 'PrevPageLink',
            computed: {
                containerClass() {
                    return ['p-paginator-prev p-paginator-element p-link', {
                        'p-disabled': this.$attrs.disabled
                    }];
                }
            },
            directives: {
                'ripple': Ripple__default['default']
            }
        };

        const _hoisted_1$5 = /*#__PURE__*/vue.createVNode("span", { class: "p-paginator-icon pi pi-angle-left" }, null, -1);

        function render$5(_ctx, _cache, $props, $setup, $data, $options) {
          const _directive_ripple = vue.resolveDirective("ripple");

          return vue.withDirectives((vue.openBlock(), vue.createBlock("button", {
            class: $options.containerClass,
            type: "button"
          }, [
            _hoisted_1$5
          ], 2)), [
            [_directive_ripple]
          ])
        }

        script$5.render = render$5;

        var script$6 = {
            name: 'RowsPerPageDropdown',
            inheritAttrs: false,
            emits: ['rows-change'],
            props: {
                options: Array,
                rows: Number
            },
            methods: {
                onChange(value) {
                    this.$emit('rows-change', value);
                }
            },
            computed: {
                rowsOptions() {
                    let opts = [];
                    if (this.options) {
                        for(let i= 0; i < this.options.length; i++) {
                            opts.push({label: String(this.options[i]), value: this.options[i]});
                        }
                    }
                    return opts;
                }
            },
            components: {
                'RPPDropdown': Dropdown__default['default']
            }
        };

        function render$6(_ctx, _cache, $props, $setup, $data, $options) {
          const _component_RPPDropdown = vue.resolveComponent("RPPDropdown");

          return (vue.openBlock(), vue.createBlock(_component_RPPDropdown, {
            modelValue: $props.rows,
            options: $options.rowsOptions,
            optionLabel: "label",
            optionValue: "value",
            "onUpdate:modelValue": _cache[1] || (_cache[1] = $event => ($options.onChange($event))),
            class: "p-paginator-rpp-options"
          }, null, 8, ["modelValue", "options"]))
        }

        script$6.render = render$6;

        var script$7 = {
            name: 'JumpToPageDropdown',
            inheritAttrs: false,
            emits: ['page-change'],
            props: {
                page: Number,
                pageCount: Number
            },
            methods: {
                onChange(value) {
                    this.$emit('page-change', value);
                }
            },
            computed: {
                pageOptions() {
                    let opts = [];
                    for(let i= 0; i < this.pageCount; i++) {
                        opts.push({label: String(i+1), value: i});
                    }
                    return opts;
                }
            },
            components: {
                'JTPDropdown': Dropdown__default['default']
            }
        };

        function render$7(_ctx, _cache, $props, $setup, $data, $options) {
          const _component_JTPDropdown = vue.resolveComponent("JTPDropdown");

          return (vue.openBlock(), vue.createBlock(_component_JTPDropdown, {
            modelValue: $props.page,
            options: $options.pageOptions,
            optionLabel: "label",
            optionValue: "value",
            "onUpdate:modelValue": _cache[1] || (_cache[1] = $event => ($options.onChange($event))),
            class: "p-paginator-page-options"
          }, null, 8, ["modelValue", "options"]))
        }

        script$7.render = render$7;

        var script$8 = {
            name: 'Paginator',
            emits: ['update:first', 'update:rows', 'page'],
            props: {
                totalRecords: {
                    type: Number,
                    default: 0
                },
                rows: {
                    type: Number,
                    default: 0
                },
                first: {
                    type: Number,
                    default: 0
                },
                pageLinkSize: {
                    type: Number,
                    default: 5
                },
                rowsPerPageOptions: {
                    type: Array,
                    default: null
                },
                template: {
                    type: String,
                    default: 'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown'
                },
                currentPageReportTemplate: {
                    type: null,
                    default: '({currentPage} of {totalPages})'
                },
                alwaysShow: {
                    type: Boolean,
                    default: true
                }
            },
            data() {
                return {
                    d_first: this.first,
                    d_rows: this.rows
                }
            },
            watch: {
                first(newValue) {
                    this.d_first = newValue;
                },
                rows(newValue) {
                    this.d_rows = newValue;
                },
                totalRecords(newValue) {
                    if (this.page > 0 && newValue && (this.d_first >= newValue)) {
                        this.changePage(this.pageCount - 1);
                    }
                }
            },
            methods: {
                changePage(p) {
                    const pc = this.pageCount;

                    if (p >= 0 && p < pc) {
                        this.d_first = this.d_rows * p;
                        const state = {
                            page: p,
                            first: this.d_first,
                            rows: this.d_rows,
                            pageCount: pc
                        };

        				this.$emit('update:first', this.d_first);
                        this.$emit('update:rows', this.d_rows);
                        this.$emit('page', state);
                    }
                },
                changePageToFirst(event) {
                    if(!this.isFirstPage) {
                        this.changePage(0);
                    }

                    event.preventDefault();
                },
                changePageToPrev(event) {
                    this.changePage(this.page - 1);
                    event.preventDefault();
                },
                changePageLink(event) {
                    this.changePage(event.value - 1);
                    event.originalEvent.preventDefault();
                },
                changePageToNext(event) {
                    this.changePage(this.page  + 1);
                    event.preventDefault();
                },
                changePageToLast(event) {
                    if(!this.isLastPage) {
                        this.changePage(this.pageCount - 1);
                    }

                    event.preventDefault();
                },
                onRowChange(value) {
                    this.d_rows = value;
                    this.changePage(this.page);
                }
            },
            computed: {
                templateItems() {
                    let keys = [];
                    this.template.split(' ').map((value) => {
                        keys.push(value.trim());
                    });
                    return keys;
                },
                page() {
                    return Math.floor(this.d_first / this.d_rows);
                },
                pageCount() {
                    return Math.ceil(this.totalRecords / this.d_rows) || 1;
                },
                isFirstPage() {
                    return this.page === 0;
                },
                isLastPage() {
                    return this.page === this.pageCount - 1;
                },
                calculatePageLinkBoundaries() {
                    const numberOfPages = this.pageCount;
                    const visiblePages = Math.min(this.pageLinkSize, numberOfPages);

                    //calculate range, keep current in middle if necessary
                    let start = Math.max(0, Math.ceil(this.page - ((visiblePages) / 2)));
                    let end = Math.min(numberOfPages - 1, start + visiblePages - 1);

                    //check when approaching to last page
                    const delta = this.pageLinkSize - (end - start + 1);
                    start = Math.max(0, start - delta);

                    return [start, end];
                },
                pageLinks() {
                    let pageLinks = [];
                    let boundaries = this.calculatePageLinkBoundaries;
                    let start = boundaries[0];
                    let end = boundaries[1];

                    for(var i = start; i <= end; i++) {
                        pageLinks.push(i + 1);
                    }

                    return pageLinks;
                },
                currentState() {
                    return {
                        page: this.page,
                        first: this.d_first,
                        rows: this.d_rows
                    }
                }
            },
            components: {
                'CurrentPageReport': script,
                'FirstPageLink': script$1,
                'LastPageLink': script$2,
                'NextPageLink': script$3,
                'PageLinks': script$4,
                'PrevPageLink': script$5,
                'RowsPerPageDropdown': script$6,
                'JumpToPageDropdown': script$7
            }
        };

        const _hoisted_1$6 = {
          key: 0,
          class: "p-paginator p-component"
        };
        const _hoisted_2 = {
          key: 0,
          class: "p-paginator-left-content"
        };
        const _hoisted_3 = {
          key: 1,
          class: "p-paginator-right-content"
        };

        function render$8(_ctx, _cache, $props, $setup, $data, $options) {
          const _component_FirstPageLink = vue.resolveComponent("FirstPageLink");
          const _component_PrevPageLink = vue.resolveComponent("PrevPageLink");
          const _component_NextPageLink = vue.resolveComponent("NextPageLink");
          const _component_LastPageLink = vue.resolveComponent("LastPageLink");
          const _component_PageLinks = vue.resolveComponent("PageLinks");
          const _component_CurrentPageReport = vue.resolveComponent("CurrentPageReport");
          const _component_RowsPerPageDropdown = vue.resolveComponent("RowsPerPageDropdown");
          const _component_JumpToPageDropdown = vue.resolveComponent("JumpToPageDropdown");

          return ($props.alwaysShow ? true : ($options.pageLinks && $options.pageLinks.length > 1))
            ? (vue.openBlock(), vue.createBlock("div", _hoisted_1$6, [
                (_ctx.$slots.left)
                  ? (vue.openBlock(), vue.createBlock("div", _hoisted_2, [
                      vue.renderSlot(_ctx.$slots, "left", { state: $options.currentState })
                    ]))
                  : vue.createCommentVNode("", true),
                (vue.openBlock(true), vue.createBlock(vue.Fragment, null, vue.renderList($options.templateItems, (item) => {
                  return (vue.openBlock(), vue.createBlock(vue.Fragment, { key: item }, [
                    (item === 'FirstPageLink')
                      ? (vue.openBlock(), vue.createBlock(_component_FirstPageLink, {
                          key: 0,
                          onClick: _cache[1] || (_cache[1] = $event => ($options.changePageToFirst($event))),
                          disabled: $options.isFirstPage
                        }, null, 8, ["disabled"]))
                      : (item === 'PrevPageLink')
                        ? (vue.openBlock(), vue.createBlock(_component_PrevPageLink, {
                            key: 1,
                            onClick: _cache[2] || (_cache[2] = $event => ($options.changePageToPrev($event))),
                            disabled: $options.isFirstPage
                          }, null, 8, ["disabled"]))
                        : (item === 'NextPageLink')
                          ? (vue.openBlock(), vue.createBlock(_component_NextPageLink, {
                              key: 2,
                              onClick: _cache[3] || (_cache[3] = $event => ($options.changePageToNext($event))),
                              disabled: $options.isLastPage
                            }, null, 8, ["disabled"]))
                          : (item === 'LastPageLink')
                            ? (vue.openBlock(), vue.createBlock(_component_LastPageLink, {
                                key: 3,
                                onClick: _cache[4] || (_cache[4] = $event => ($options.changePageToLast($event))),
                                disabled: $options.isLastPage
                              }, null, 8, ["disabled"]))
                            : (item === 'PageLinks')
                              ? (vue.openBlock(), vue.createBlock(_component_PageLinks, {
                                  key: 4,
                                  value: $options.pageLinks,
                                  page: $options.page,
                                  onClick: _cache[5] || (_cache[5] = $event => ($options.changePageLink($event)))
                                }, null, 8, ["value", "page"]))
                              : (item === 'CurrentPageReport')
                                ? (vue.openBlock(), vue.createBlock(_component_CurrentPageReport, {
                                    key: 5,
                                    template: $props.currentPageReportTemplate,
                                    page: $options.page,
                                    pageCount: $options.pageCount,
                                    first: $data.d_first,
                                    rows: $data.d_rows,
                                    totalRecords: $props.totalRecords
                                  }, null, 8, ["template", "page", "pageCount", "first", "rows", "totalRecords"]))
                                : (item === 'RowsPerPageDropdown' && $props.rowsPerPageOptions)
                                  ? (vue.openBlock(), vue.createBlock(_component_RowsPerPageDropdown, {
                                      key: 6,
                                      rows: $data.d_rows,
                                      options: $props.rowsPerPageOptions,
                                      onRowsChange: _cache[6] || (_cache[6] = $event => ($options.onRowChange($event)))
                                    }, null, 8, ["rows", "options"]))
                                  : (item === 'JumpToPageDropdown')
                                    ? (vue.openBlock(), vue.createBlock(_component_JumpToPageDropdown, {
                                        key: 7,
                                        page: $options.page,
                                        pageCount: $options.pageCount,
                                        onPageChange: _cache[7] || (_cache[7] = $event => ($options.changePage($event)))
                                      }, null, 8, ["page", "pageCount"]))
                                    : vue.createCommentVNode("", true)
                  ], 64))
                }), 128)),
                (_ctx.$slots.right)
                  ? (vue.openBlock(), vue.createBlock("div", _hoisted_3, [
                      vue.renderSlot(_ctx.$slots, "right", { state: $options.currentState })
                    ]))
                  : vue.createCommentVNode("", true)
              ]))
            : vue.createCommentVNode("", true)
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

        var css_248z = "\n.p-paginator {\n    display: -webkit-box;\n    display: -ms-flexbox;\n    display: flex;\n    -webkit-box-align: center;\n        -ms-flex-align: center;\n            align-items: center;\n    -webkit-box-pack: center;\n        -ms-flex-pack: center;\n            justify-content: center;\n    -ms-flex-wrap: wrap;\n        flex-wrap: wrap;\n}\n.p-paginator-left-content {\n\tmargin-right: auto;\n}\n.p-paginator-right-content {\n\tmargin-left: auto;\n}\n.p-paginator-page,\n.p-paginator-next,\n.p-paginator-last,\n.p-paginator-first,\n.p-paginator-prev,\n.p-paginator-current {\n    cursor: pointer;\n    display: -webkit-inline-box;\n    display: -ms-inline-flexbox;\n    display: inline-flex;\n    -webkit-box-align: center;\n        -ms-flex-align: center;\n            align-items: center;\n    -webkit-box-pack: center;\n        -ms-flex-pack: center;\n            justify-content: center;\n    line-height: 1;\n    -webkit-user-select: none;\n       -moz-user-select: none;\n        -ms-user-select: none;\n            user-select: none;\n    overflow: hidden;\n    position: relative;\n}\n.p-paginator-element:focus {\n    z-index: 1;\n    position: relative;\n}\n";
        styleInject(css_248z);

        script$8.render = render$8;

        return script$8;

}(Vue, primevue.ripple, primevue.dropdown));
