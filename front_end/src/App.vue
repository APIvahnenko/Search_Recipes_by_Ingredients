<template>
  <div id="app">
    <div class="home col">
      <section class="first row" :class="{'shadow':isShowShadow}">
        <el-autocomplete
                class="search"
                v-model="inputValue"
                :fetch-suggestions="querySearch"
                placeholder="please input your ingredient"
                @select="handleSelect"
        >
          <!--这里是搜索框的内容-->
          <!--select这里会显示所选的内容-->
          <el-button slot="append" icon="el-icon-search" @click="handleSearchClick"></el-button>
        </el-autocomplete>
      </section>
      <section class="second col">
        <!-- 下拉折叠区域 -->
        <section class="collapse-area">
          <div class="triangle" @click="foldAll">
            <div class="triangle-item" :class="{'rotate':isCollapse}"></div>
            <span style="margin-left:15px;" class="text-color">Select What You Want</span>
          </div>
          <el-collapse
                  v-model="activeNames"
                  @change="handleChange"
                  v-if="isCollapse"
                  class="collapse-panel"
          >
            <el-collapse-item :name="index" v-for="(item,index) in checkData" :key="index">
              <p style="margin-left:15px;" slot="title">
                <el-icon
                        class="el-icon-arrow-right"
                        :class="{'rotate':activeNames.includes(index)}"
                ></el-icon>
                {{item.title}}
              </p>
              <el-row>
                <el-col :span="8" v-for="(sub,key) in item.check" :key="key">
                  <el-checkbox :label="sub" @change="handleAddCheck(sub)"></el-checkbox>
                </el-col>
              </el-row>
            </el-collapse-item>
          </el-collapse>
        </section>
      </section>
      <!-- 图片展示区域 -->
      <section class="third col">
        <transition name="el-fade-in-linear">
          <div class="img-contaienr row" v-show="imgs.length">
            <div
                    class="img-item"
                    v-for="item in imgs"
                    :key="item.id"
                    @mouseover="() => handleImageHover(item)"
                    @mouseout="() => handleImageOut(item)"
            >
              <el-image :src="item.src">
                <div slot="placeholder" class="image-slot">
                  <!-- loading<span class="dot">...</span> -->
                  <span v-for="desc in item.desc" :key="desc">{{desc}}</span>
                </div>
              </el-image>
              <div class="img-hover-info" v-show="item.isHover">{{ item.desc }}</div>
            </div>
          </div>
        </transition>
        <el-button class="footer-btn" icon="el-icon-arrow-down" circle @click="refreshClick"></el-button>
        <back-to-top></back-to-top>
      </section>
	</div>
  </div>
  
</template>

<script>
  import DataList from "./assets/dataList.js";
  import BackToTop from "./components/backToTop";
  const testData1 = [
    {
      id: 1,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "hi testdata1"
    },
    {
      id: 2,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 3,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 4,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 5,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 6,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 7,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 8,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    },
    {
      id: 9,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      desc: "图片描述"
    }
  ];
  const testData2 = [
    {
      id: 1,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "hi testdata 2"
    },
    {
      id: 2,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 3,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 4,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 5,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 6,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 7,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 8,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 9,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    }
  ];
  const tempFlag = {
    search: true,
    refresh: true
  };
  // @ is an alias to /src
  import axios from "axios";
  export default {
    name: "home",
    components: { BackToTop },
    data() {
      return {
        isShowShadow: false,
        isCollapse: false,
        imgs: [],
		//added part
		recipe_ids: [],
		length_recipe_ids : "",
		recipe_idslist:[],
		counter : 0,
		check_imgs : [],
		//end added part
        inputValue: "",
        activeNames: [0],
        selectCheck: [],
        checkData: DataList.checkBox,
        checkList: []
      };
    },
    computed: {
      isRotate() {
        // var index = this.activeNames.indexOf("0");
        if (this.activeNames.length > 0) {
          return true;
        } else {
          return false;
        }
      },
	},
    mounted() {
      //this.getData();
      this.imgs = testData1;
      window.addEventListener("scroll", this.handleScroll, true);
    },
    destroyed() {
      window.removeEventListener("scroll", this.handleScroll, true);
    },
    methods: {
      //监听页面下滚150px
      handleScroll(e) {
        const scrollTop =
            document.documentElement.scrollTop || document.body.Scroller;
        this.isShowShadow = scrollTop > 0;
      },
      handleAddCheck(value) {
        var index = this.selectCheck.indexOf(value);
        if (index >= 0) {
          this.selectCheck.splice(index, 1);
        } else {
          this.selectCheck.push(value);
        }
      },
	  async retrieveData(){
	  //var recipe_idslist = [];
	  var local_counter = this.counter+10;
	  while(this.counter<local_counter){
			if(this.counter <this.length_recipe_ids){
		this.recipe_idslist.push(this.recipe_ids[this.counter]);
		this.counter++;
		}
	  }
	  
	  this.recipe_idslist = this.recipe_idslist.toString();
	  try{
	  const response = await axios.get("http://127.0.0.1:5000/retrieve", {params: {recipe_list:this.recipe_idslist,city:'None'}});
	  //.then((response) => {
		//let res = response.data;
		console.log(response.data);
		this.check_imgs = response.data.recipe_info;
	  //})
	  }catch(error){
				console.error(error);
		}
		
	  //var imgs_length = this.check_imgs.length;
	  //var i = 0;
	  //while(imgs_length < 9){
		//	this,check_imgs.push(testData1[i]);
			//i++;
			//imgs_length++;
		//}
		//this.imgs = this.check_imgs;
		this.recipe_idslist = [];
	  },
      async getData() {
		try{
         const response = await axios.get("http://127.0.0.1:5000/test", {
              // 传递参数
              params: {
                city: 'hi',
				recipe:'whatsup'
              }
            });
            //.then((response) => {
              // 请求成功
              //let res = response.data;
         console.log(response.data);
              //这个res就是请求回来的数据，可以在控制台看到，下面是修改了一条图片描述
              this.recipe_ids = response.data.id;
			  this.length_recipe_ids = response.data.length;
			  this.retrieveData();
              //this.imgs[0].desc = res.data;
            //})
			}catch(error){
				console.error(error);
			}
	  },
      //每次取的时候先写个函数去修改它的key，image1=image+'1'这样
	
      async handleSearchClick() {
        this.getData();
		//this.imgs[0].desc=this.check_imgs[0].desc;
		//this.retrieveData();
        //tempFlag.refresh = !tempFlag.refresh;
		
		this.imgs = this.check_imgs;
		//this.imgs[0].desc = this.recipe_idslist;
		//this.imgs[0].desc = this.res.data;
      },
      refreshClick() {
		this.retrieveData();
        //tempFlag.search = !tempFlag.search;
        const arr = this.imgs.concat(this.check_imgs);
        this.imgs = arr;
      },
      handleImageHover(item) {
        this.$set(item, "isHover", true);
      },
      handleImageOut(item) {
        this.$set(item, "isHover", false);
      },
      querySearch(queryString, cb) {
        var checkList = this.checkList.map(item => ({ value: item }));
        var results = queryString
            ? checkList.filter(this.createFilter(queryString))
            : checkList;
        cb(results);
      },
      createFilter(queryString) {
        return checkList => {
          return (
              checkList.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
          );
        };
      },
      handleSelect(item) {
        console.log(item);
      },
      handleChange() {},
      foldAll() {
        if (this.isCollapse) {
          this.activeNames = [];
          this.isCollapse = false;
        } else {
          this.isCollapse = true;
          this.activeNames = [0];
        }
      }
    }
  };
</script>

<style lang="less" scoped>
  html {
    padding: 0px;
    margin: 0px;
  } /*这是把白边去掉的方法*/
  html,
  #app::-webkit-scrollbar {
    display: none;
  }
  #app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  /*.isScroll {
    background: linear-gradient(
            to right,
            rgba(30, 87, 153, 0.8) 0%,
            rgba(30, 87, 153, 0.8) 44%,
            rgba(41, 137, 216, 0.8) 94%
    ) !important; !* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ *!
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc1e5799', endColorstr='#cc2989d8',GradientType=1 );
  }*/
  .col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .row {
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    align-items: center;
  }
  .home {
    //背景
    width: 100%;
    width: 100%;
    background: black;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: 100% 100%;
    .first {
      position: fixed;
      top: 0;
      z-index: 100;
      width: 100%;
      .search {
        width: 500px;
        margin-top: 30px;
        margin-bottom: 30px;
      }
    }
    .shadow {
      box-shadow: 1px 1px 3px black;
      background-color: black !important;
      background-image: linear-gradient(180deg, black 19%, black 80%) !important;
    }
    .second {
      box-sizing: border-box;
      padding: 30px 350px 0 350px;
      width: 100%;
      .collapse-area {
        margin-top: 100px;
        width: 1250px;
        opacity: 0.5;
      }
      .collapse-panel {
        animation-name: fadeIn; /*动画名称*/
        animation-duration: 0.5s; /*动画持续时间*/
        animation-iteration-count: 1; /*动画次数*/
        animation-delay: 0s; /*延迟时间*/
      }
    }

    .third {
      .img-contaienr {
        width: 1250px;
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
            background: rgba(255, 165, 79, 0.5);
            text-align: center;
            line-height: 253px;
            color: #fff;
          }
        }
      }
    }
    .footer-btn {
      margin-top: 30px;
    }
  }
  .triangle {
    //width: 100%;
    height: 30px;
    line-height: 30px;
    font-size: 30px;
    text-align: left;
    display: flex;
    align-items: center;
    cursor: pointer;
    .triangle-item {
      width: 0;
      height: 0;
      overflow: hidden;
      border-left: 10px solid #FFFFFF;
      border-top: 10px solid transparent;
      border-bottom: 10px solid transparent;
      transition: transform 0.2s ease-in;
    }
  }
  /deep/.el-collapse-item__arrow {
    display: none !important;
  }
  .rotate {
    transform: rotate(90deg);
    transition: transform 0.2s ease-in;
  }
  @keyframes fadeIn {
    0% {
      opacity: 0; /*初始状态 透明度为0*/
    }
    50% {
      opacity: 0.5; /*中间状态 透明度为0*/
    }
    100% {
      opacity: 1; /*结尾状态 透明度为1*/
    }
  }
  .text-color{
    color: white;
    font-family: "Times New Roman"
  }
</style>
