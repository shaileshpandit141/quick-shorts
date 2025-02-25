(self.webpackChunkfrontend = self.webpackChunkfrontend || []).push([
  [333],
  {
    5333: (o, e, l) => {
      l.r(e), l.d(e, { default: () => n });
      var i = l(1338),
        t = l(6723);
      const n = (0, i.A)(
        (0, t.jsx)("path", {
          d: "M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6",
        }),
        "Settings",
      );
    },
    1338: (o, e, l) => {
      l.d(e, { A: () => y });
      var i = l(9379),
        t = l(2483),
        n = l(3986),
        r = l(9765),
        c = l(7266),
        s = l(1251),
        a = l(7927),
        d = l(6751),
        v = l(6518),
        u = l(292),
        p = l(1431);
      function f(o) {
        return (0, p.Ay)("MuiSvgIcon", o);
      }
      (0, u.A)("MuiSvgIcon", [
        "root",
        "colorPrimary",
        "colorSecondary",
        "colorAction",
        "colorError",
        "colorDisabled",
        "fontSizeInherit",
        "fontSizeSmall",
        "fontSizeMedium",
        "fontSizeLarge",
      ]);
      var m = l(6723);
      const h = [
          "children",
          "className",
          "color",
          "component",
          "fontSize",
          "htmlColor",
          "inheritViewBox",
          "titleAccess",
          "viewBox",
        ],
        S = (0, a.Ay)("svg", {
          name: "MuiSvgIcon",
          slot: "Root",
          overridesResolver: (o, e) => {
            const { ownerState: l } = o;
            return [
              e.root,
              "inherit" !== l.color && e["color".concat((0, s.A)(l.color))],
              e["fontSize".concat((0, s.A)(l.fontSize))],
            ];
          },
        })(
          (0, d.A)((o) => {
            var e, l, i, t, n, r, c, s, a, d, v, u, p, f, m;
            let { theme: h } = o;
            return {
              userSelect: "none",
              width: "1em",
              height: "1em",
              display: "inline-block",
              flexShrink: 0,
              transition:
                null === (e = h.transitions) ||
                void 0 === e ||
                null === (l = e.create) ||
                void 0 === l
                  ? void 0
                  : l.call(e, "fill", {
                      duration:
                        null ===
                          (i = (null !== (t = h.vars) && void 0 !== t ? t : h)
                            .transitions) ||
                        void 0 === i ||
                        null === (i = i.duration) ||
                        void 0 === i
                          ? void 0
                          : i.shorter,
                    }),
              variants: [
                {
                  props: (o) => !o.hasSvgAsChild,
                  style: { fill: "currentColor" },
                },
                {
                  props: { fontSize: "inherit" },
                  style: { fontSize: "inherit" },
                },
                {
                  props: { fontSize: "small" },
                  style: {
                    fontSize:
                      (null === (n = h.typography) ||
                      void 0 === n ||
                      null === (r = n.pxToRem) ||
                      void 0 === r
                        ? void 0
                        : r.call(n, 20)) || "1.25rem",
                  },
                },
                {
                  props: { fontSize: "medium" },
                  style: {
                    fontSize:
                      (null === (c = h.typography) ||
                      void 0 === c ||
                      null === (s = c.pxToRem) ||
                      void 0 === s
                        ? void 0
                        : s.call(c, 24)) || "1.5rem",
                  },
                },
                {
                  props: { fontSize: "large" },
                  style: {
                    fontSize:
                      (null === (a = h.typography) ||
                      void 0 === a ||
                      null === (d = a.pxToRem) ||
                      void 0 === d
                        ? void 0
                        : d.call(a, 35)) || "2.1875rem",
                  },
                },
                ...Object.entries(
                  (null !== (v = h.vars) && void 0 !== v ? v : h).palette,
                )
                  .filter((o) => {
                    let [, e] = o;
                    return e && e.main;
                  })
                  .map((o) => {
                    var e, l;
                    let [i] = o;
                    return {
                      props: { color: i },
                      style: {
                        color:
                          null ===
                            (e = (null !== (l = h.vars) && void 0 !== l ? l : h)
                              .palette) ||
                          void 0 === e ||
                          null === (e = e[i]) ||
                          void 0 === e
                            ? void 0
                            : e.main,
                      },
                    };
                  }),
                {
                  props: { color: "action" },
                  style: {
                    color:
                      null ===
                        (u = (null !== (p = h.vars) && void 0 !== p ? p : h)
                          .palette) ||
                      void 0 === u ||
                      null === (u = u.action) ||
                      void 0 === u
                        ? void 0
                        : u.active,
                  },
                },
                {
                  props: { color: "disabled" },
                  style: {
                    color:
                      null ===
                        (f = (null !== (m = h.vars) && void 0 !== m ? m : h)
                          .palette) ||
                      void 0 === f ||
                      null === (f = f.action) ||
                      void 0 === f
                        ? void 0
                        : f.disabled,
                  },
                },
                { props: { color: "inherit" }, style: { color: void 0 } },
              ],
            };
          }),
        ),
        A = t.forwardRef(function (o, e) {
          const l = (0, v.b)({ props: o, name: "MuiSvgIcon" }),
            {
              children: a,
              className: d,
              color: u = "inherit",
              component: p = "svg",
              fontSize: A = "medium",
              htmlColor: z,
              inheritViewBox: y = !1,
              titleAccess: g,
              viewBox: x = "0 0 24 24",
            } = l,
            w = (0, n.A)(l, h),
            b = t.isValidElement(a) && "svg" === a.type,
            B = (0, i.A)(
              (0, i.A)({}, l),
              {},
              {
                color: u,
                component: p,
                fontSize: A,
                instanceFontSize: o.fontSize,
                inheritViewBox: y,
                viewBox: x,
                hasSvgAsChild: b,
              },
            ),
            C = {};
          y || (C.viewBox = x);
          const I = ((o) => {
            const { color: e, fontSize: l, classes: i } = o,
              t = {
                root: [
                  "root",
                  "inherit" !== e && "color".concat((0, s.A)(e)),
                  "fontSize".concat((0, s.A)(l)),
                ],
              };
            return (0, c.A)(t, f, i);
          })(B);
          return (0, m.jsxs)(
            S,
            (0, i.A)(
              (0, i.A)(
                (0, i.A)(
                  (0, i.A)(
                    {
                      as: p,
                      className: (0, r.A)(I.root, d),
                      focusable: "false",
                      color: z,
                      "aria-hidden": !g || void 0,
                      role: g ? "img" : void 0,
                      ref: e,
                    },
                    C,
                  ),
                  w,
                ),
                b && a.props,
              ),
              {},
              {
                ownerState: B,
                children: [
                  b ? a.props.children : a,
                  g ? (0, m.jsx)("title", { children: g }) : null,
                ],
              },
            ),
          );
        });
      A.muiName = "SvgIcon";
      const z = A;
      function y(o, e) {
        function l(l, t) {
          return (0, m.jsx)(
            z,
            (0, i.A)(
              (0, i.A)({ "data-testid": "".concat(e, "Icon"), ref: t }, l),
              {},
              { children: o },
            ),
          );
        }
        return (l.muiName = z.muiName), t.memo(t.forwardRef(l));
      }
    },
  },
]);
//# sourceMappingURL=333.f0b6e571.chunk.js.map
