class Ut {
    /**
    * 异步延迟
    * @param {number} time 延迟的时间,单位毫秒
    */
    static sleep(time = 0) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve();
        }, time);
      })
    };
  }
  
  module.exports = Ut;