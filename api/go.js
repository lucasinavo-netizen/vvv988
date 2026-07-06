const TARGET = "https://www.myan99.me/m/home?affiliateCode=seom202";

module.exports = function handler(_req, res) {
  res.setHeader("X-Robots-Tag", "noindex, nofollow");
  res.setHeader("Cache-Control", "no-store");
  res.writeHead(302, { Location: TARGET });
  res.end();
};
