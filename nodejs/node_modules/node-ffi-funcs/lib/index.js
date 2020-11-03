const os = require('os')
module.exports = /Darwin/.test(os.type()) ? require('./darwin') : require('./win32')
