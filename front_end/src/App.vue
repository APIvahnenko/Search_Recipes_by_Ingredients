<template>
  <div id="app">
    <div class="home">
      <div class="page-area">
        <el-input placeholder="请输入内容" v-model="inputValue" class="search">
          <el-button slot="append" icon="el-icon-search" @click="handleSearchClick"></el-button>
        </el-input>

        <!-- 下拉折叠区域 -->
        <section class="collapse-area">
          <el-collapse v-model="activeNames" @change="handleChange" accordion>
            <el-collapse-item title="pantry" name="1">
              <el-checkbox-group v-model="checkList">
                <el-checkbox label="复选框 A"></el-checkbox>
                <el-checkbox label="复选框 B"></el-checkbox>
                <el-checkbox label="复选框 C"></el-checkbox>
                <el-checkbox label="禁用" disabled></el-checkbox>
                <el-checkbox label="选中且禁用" disabled></el-checkbox>
              </el-checkbox-group>
            </el-collapse-item>
            <el-collapse-item title="grain" name="2">
              <el-checkbox-group v-model="checkList">
                <el-checkbox label="复选框 A"></el-checkbox>
                <el-checkbox label="复选框 B"></el-checkbox>
                <el-checkbox label="复选框 C"></el-checkbox>
                <el-checkbox label="禁用" disabled></el-checkbox>
                <el-checkbox label="选中且禁用" disabled></el-checkbox>
              </el-checkbox-group>
            </el-collapse-item>
            <el-collapse-item title="vegetable & fruit" name="3">
              <el-checkbox-group v-model="checkList">
                <el-checkbox label="复选框 A"></el-checkbox>
                <el-checkbox label="复选框 B"></el-checkbox>
                <el-checkbox label="复选框 C"></el-checkbox>
                <el-checkbox label="禁用" disabled></el-checkbox>
                <el-checkbox label="选中且禁用" disabled></el-checkbox>
              </el-checkbox-group>
            </el-collapse-item>
            <el-collapse-item title="spices" name="4">
              <el-checkbox-group v-model="checkList">
                <el-checkbox label="复选框 A"></el-checkbox>
                <el-checkbox label="复选框 B"></el-checkbox>
                <el-checkbox label="复选框 C"></el-checkbox>
                <el-checkbox label="禁用" disabled></el-checkbox>
                <el-checkbox label="选中且禁用" disabled></el-checkbox>
              </el-checkbox-group>
            </el-collapse-item>
          </el-collapse>
        </section>

        <!-- 图片展示区域 -->
        <section class="img-area">
          <transition name="el-fade-in-linear">
            <div class="img-contaienr" v-show="imgs.length">
              <div class="img-item" v-for="item in imgs" :key="item.id" @mouseover="() => handleImageHover(item)" @mouseout="() => handleImageOut(item)">
                <el-image :src="item.src">
                  <div slot="placeholder" class="image-slot">
                    <!-- loading<span class="dot">...</span> -->
                  </div>
                </el-image>
                <div class="img-hover-info" v-show="item.isHover">{{ item.desc }}</div>
              </div>
            </div>
          </transition>
        </section>
        <el-button class="footer-btn" icon="el-icon-arrow-down" circle @click="refreshClick"></el-button>
      </div>
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  import axios from 'axios'
  export default {
    name: 'home',
    components: {
    },
    data() {
      return {
        imgs: [],
        inputValue: '',
        activeNames: ['1'],
        checkList: ['选中且禁用','复选框 A']
    }
    },
    beforeRouteEnter(to, from, next) {
      // 添加背景色 margin:0;padding:0是为了解决vue四周有白边的问题
      document.querySelector('body').setAttribute('style', "margin:0;padding:0")
      next()
    },
    beforeRouteLeave(to, from, next) {
      // 去除背景色
      document.querySelector('body').setAttribute('style', '')
      next()
    },
    mounted() {
      this.getData()
      // setTimeout(() => {
      this.imgs = [
        {id: 1, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述' },
        {id: 2, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 3, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 4, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 5, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 6, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 7, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 8, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  },
        {id: 9, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '图片描述'  }
      ]
      // }, 300);
    },
    methods: {
      getData() {
        axios.get("http://wthrcdn.etouch.cn/weather_mini", {
          // 传递参数
          params: {
            city: '深圳'
          },
        }).then(response => {
          // 请求成功
          let res = response.data;
          console.log(res);
          //这个res就是请求回来的数据，可以在控制台看到，下面是修改了一条图片描述
          this.imgs[0].desc = res.data.ganmao
        })
      },
      handleSearchClick() {
        // location.reload()
        const arr = [
          {id: 1, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2' },
          {id: 2, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 3, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 4, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 5, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 6, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 7, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 8, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  },
          {id: 9, src: 'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg', desc: '图片描述2'  }
        ]
        this.imgs = arr
      },
      refreshClick() {
        const arr = this.imgs.concat(this.imgs)
        this.imgs = arr
      },
      handleImageHover(item) {
        this.$set(item,'isHover',true)
      },
      handleImageOut(item) {
        this.$set(item,'isHover',false)
      }
    }
  }
</script>

<style lang="less" scoped>

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  .home {
    display: flex;
    justify-content: center;
    align-items: center;

    //背景
   /* background: url('https://images.unsplash.com/photo-1546548970-71785318a17b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=600&q=60');*/
    background: black;
    background-attachment:fixed;
    background-repeat: no-repeat;

    .page-area {
      width: 1280px;
      .search {
        width: 500px;
        margin-top: 30px;
      }
      .collapse-area {
        margin-top: 70px;
      }
      .img-area {
        min-height: 700px;
        .img-contaienr {
          display: flex;
          justify-content: center;
          align-items: center;
          flex-wrap: wrap;
          margin-top: 80px;
          .img-item {
            width: 380px;
            margin: 0px 2px;
            position: relative;
            .img-hover-info {
              width: 380px;
              height: 253px;
              position: absolute;
              top: 0px;
              left: 0px;
              background: rgba(0, 0, 0, .5);
              text-align: center;
              line-height: 253px;
              color: #FFF;
            }
          }
        }
      }
    }
    .footer-btn {
      margin-top: 30px;
    }
  }
</style>
