//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    array: [],
    imgUrls: [
      'https://modao.cc/uploads3/images/2093/20933515/raw_1527769874.jpeg',
      'https://modao.cc/uploads3/images/2093/20933520/raw_1527769876.jpeg',
      'https://modao.cc/uploads3/images/2093/20933523/raw_1527769880.jpeg'
    ],
    indicatorDots: true,
    autoplay: true,
    interval: 3000,
    duration: 1000
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  handleDelete: function(e) {
    var element = e.currentTarget;
    var that = this;
    wx.request({
      url: 'http://localhost:8080/delete',
      data: {id: element.dataset.id},
      method: 'GET',
      success: function (res) {
        wx.reLaunch({
          url: '../index/index'
        });
      }
    });
  },
  onLoad: function () {
    var that = this;
    wx.request({
      url: 'http://localhost:8080/find',
      data: {},
      method: 'GET',
      success: function(res) {
        that.setData({
          'array': res.data.data
        })
      }
    });
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  changeIndicatorDots: function (e) {
    this.setData({
      indicatorDots: !this.data.indicatorDots
    })
  },
  changeAutoplay: function (e) {
    this.setData({
      autoplay: !this.data.autoplay
    })
  },
  intervalChange: function (e) {
    this.setData({
      interval: e.detail.value
    })
  },
  durationChange: function (e) {
    this.setData({
      duration: e.detail.value
    })
  }
})
