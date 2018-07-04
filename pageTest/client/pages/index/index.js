//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    array: [{
      content: 'text1'
    }, {
      content: 'text2'
    }, {
      content: 'text3'
    }]
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
  }
})
