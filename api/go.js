const TARGET = "https://www.rr95k.com/?ch=0cf28df51e";

module.exports = function handler(_req, res) {
  res.setHeader("X-Robots-Tag", "noindex, nofollow");
  res.setHeader("Cache-Control", "no-store");
  res.writeHead(302, { Location: TARGET });
  res.end();
};
