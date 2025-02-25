(self.webpackChunkfrontend = self.webpackChunkfrontend || []).push([
  [623],
  {
    9623: (s, e, a) => {
      a.r(e), a.d(e, { default: () => m });
      var n = a(2483),
        i = a(4666),
        r = a(149),
        o = a(7351),
        d = a(5250),
        l = a(9929),
        t = a(8940),
        c = a(6723);
      const m = () => {
        const s = (0, i.Zp)(),
          { status: e, message: a, errors: m } = (0, l.y8)(),
          [p, h] = (0, r.MY)({ email: "", password: "" });
        return (
          (0, n.useEffect)(() => {
            "succeeded" === e
              ? ((0, t.aT)("success", a), s("/home"))
              : "failed" === e && ((0, t.aT)("error", a), (0, l.FW)());
          }, [e, a, s]),
          (0, o.w)()
            ? (0, c.jsx)(i.C5, { to: "/home" })
            : (0, c.jsxs)("div", {
                className: "signin-page",
                children: [
                  (0, c.jsxs)("div", {
                    className: "header",
                    children: [
                      (0, c.jsx)("h3", {
                        className: "form-label",
                        children: "Sign in",
                      }),
                      (0, c.jsx)("p", {
                        className: "form-description",
                        children: "Sign in with your existing credentials.",
                      }),
                    ],
                  }),
                  (0, c.jsxs)("form", {
                    className: "form",
                    onSubmit: (s) => {
                      s.preventDefault(), (0, l.kv)(p);
                    },
                    children: [
                      (0, c.jsx)(d.EL, {}),
                      (0, c.jsx)(d.pd, {
                        name: "email",
                        type: "text",
                        value: p.email,
                        onChange: h,
                        isDisabled: "loading" === e,
                      }),
                      (0, c.jsx)(d.pd, {
                        name: "password",
                        type: "password",
                        value: p.password,
                        onChange: h,
                        isDisabled: "loading" === e,
                      }),
                      (0, c.jsx)(d.q_, { field: "none", errors: m }),
                      (0, c.jsxs)("div", {
                        className: "split-container",
                        children: [
                          (0, c.jsx)("span", {}),
                          (0, c.jsx)(i.N_, {
                            to: "/forgot-password",
                            children: "Forgot password",
                          }),
                        ],
                      }),
                      (0, c.jsxs)("div", {
                        className: "actions",
                        children: [
                          (0, c.jsx)(d.Z2, {}),
                          (0, c.jsx)(d.$n, {
                            type: "submit",
                            iconName: "signin",
                            className: "button",
                            isLoaderOn: "loading" === e,
                            children: "sign in",
                          }),
                        ],
                      }),
                    ],
                  }),
                ],
              })
        );
      };
    },
  },
]);
//# sourceMappingURL=623.c3393e9a.chunk.js.map
