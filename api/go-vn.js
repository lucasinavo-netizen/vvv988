// Vietnam affiliate redirect. Keep the partner URL out of public HTML.
const TARGET = "https://www.v123888.com/agent/AUKMEH";

module.exports = (req, res) => {
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  res.writeHead(302, {
    Location: TARGET,
    'Cache-Control': 'no-store, no-cache, must-revalidate',
  });
  res.end();
};
