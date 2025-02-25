(self.webpackChunkfrontend = self.webpackChunkfrontend || []).push([
  [295],
  {
    4295: (o, e, i) => {
      i.r(e), i.d(e, { default: () => n });
      var l = i(1338),
        r = i(6723);
      const n = (0, l.A)(
        [
          (0, r.jsx)("circle", { cx: "12", cy: "6", r: "2" }, "0"),
          (0, r.jsx)("circle", { cx: "6", cy: "18", r: "2" }, "1"),
          (0, r.jsx)("circle", { cx: "6", cy: "12", r: "2" }, "2"),
          (0, r.jsx)("circle", { cx: "6", cy: "6", r: "2" }, "3"),
          (0, r.jsx)("circle", { cx: "18", cy: "6", r: "2" }, "4"),
          (0, r.jsx)(
            "path",
            {
              d: "M11 18.07v1.43c0 .28.22.5.5.5h1.4c.13 0 .26-.05.35-.15l5.83-5.83-2.12-2.12-5.81 5.81c-.1.1-.15.23-.15.36M12.03 14 14 12.03V12c0-1.1-.9-2-2-2s-2 .9-2 2 .9 2 2 2zm8.82-2.44-1.41-1.41c-.2-.2-.51-.2-.71 0l-1.06 1.06 2.12 2.12 1.06-1.06c.2-.2.2-.51 0-.71",
            },
            "5",
          ),
        ],
        "AppRegistrationRounded",
      );
    },
    1338: (o, e, i) => {
      i.d(e, { A: () => x });
      var l = i(9379),
        r = i(2483),
        n = i(3986),
        t = i(9765),
        c = i(7266),
        s = i(1251),
        a = i(7927),
        d = i(6751),
        v = i(6518),
        u = i(292),
        p = i(1431);
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
      var m = i(6723);
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
            const { ownerState: i } = o;
            return [
              e.root,
              "inherit" !== i.color && e["color".concat((0, s.A)(i.color))],
              e["fontSize".concat((0, s.A)(i.fontSize))],
            ];
          },
        })(
          (0, d.A)((o) => {
            var e, i, l, r, n, t, c, s, a, d, v, u, p, f, m;
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
                null === (i = e.create) ||
                void 0 === i
                  ? void 0
                  : i.call(e, "fill", {
                      duration:
                        null ===
                          (l = (null !== (r = h.vars) && void 0 !== r ? r : h)
                            .transitions) ||
                        void 0 === l ||
                        null === (l = l.duration) ||
                        void 0 === l
                          ? void 0
                          : l.shorter,
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
                      null === (t = n.pxToRem) ||
                      void 0 === t
                        ? void 0
                        : t.call(n, 20)) || "1.25rem",
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
                    var e, i;
                    let [l] = o;
                    return {
                      props: { color: l },
                      style: {
                        color:
                          null ===
                            (e = (null !== (i = h.vars) && void 0 !== i ? i : h)
                              .palette) ||
                          void 0 === e ||
                          null === (e = e[l]) ||
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
        A = r.forwardRef(function (o, e) {
          const i = (0, v.b)({ props: o, name: "MuiSvgIcon" }),
            {
              children: a,
              className: d,
              color: u = "inherit",
              component: p = "svg",
              fontSize: A = "medium",
              htmlColor: y,
              inheritViewBox: x = !1,
              titleAccess: z,
              viewBox: g = "0 0 24 24",
            } = i,
            w = (0, n.A)(i, h),
            j = r.isValidElement(a) && "svg" === a.type,
            b = (0, l.A)(
              (0, l.A)({}, i),
              {},
              {
                color: u,
                component: p,
                fontSize: A,
                instanceFontSize: o.fontSize,
                inheritViewBox: x,
                viewBox: g,
                hasSvgAsChild: j,
              },
            ),
            R = {};
          x || (R.viewBox = g);
          const B = ((o) => {
            const { color: e, fontSize: i, classes: l } = o,
              r = {
                root: [
                  "root",
                  "inherit" !== e && "color".concat((0, s.A)(e)),
                  "fontSize".concat((0, s.A)(i)),
                ],
              };
            return (0, c.A)(r, f, l);
          })(b);
          return (0, m.jsxs)(
            S,
            (0, l.A)(
              (0, l.A)(
                (0, l.A)(
                  (0, l.A)(
                    {
                      as: p,
                      className: (0, t.A)(B.root, d),
                      focusable: "false",
                      color: y,
                      "aria-hidden": !z || void 0,
                      role: z ? "img" : void 0,
                      ref: e,
                    },
                    R,
                  ),
                  w,
                ),
                j && a.props,
              ),
              {},
              {
                ownerState: b,
                children: [
                  j ? a.props.children : a,
                  z ? (0, m.jsx)("title", { children: z }) : null,
                ],
              },
            ),
          );
        });
      A.muiName = "SvgIcon";
      const y = A;
      function x(o, e) {
        function i(i, r) {
          return (0, m.jsx)(
            y,
            (0, l.A)(
              (0, l.A)({ "data-testid": "".concat(e, "Icon"), ref: r }, i),
              {},
              { children: o },
            ),
          );
        }
        return (i.muiName = y.muiName), r.memo(r.forwardRef(i));
      }
    },
  },
]);
//# sourceMappingURL=295.3c28737f.chunk.js.map
