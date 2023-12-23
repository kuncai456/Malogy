import axios from "axios";
import util from './utils';

export default {
    // mixins: [baseMixin],
    name: "ActivityBase",
    data() {
        return {
            tabPosition: 'left',
            active: 'tab1',
            envlist: [
                { "label": "dev", "value": 'dev' },
                { "label": "test", "value": 'test' },
                { "label": "pre", "value": 'pre' },
                { "label": "prod", "value": 'prod' }
            ],
            authCountrys: [
                { "label": '英国', "value": 200 },
                { "label": "韩国", "value": 94 },
                { "label": '日本', "value": 89 },
            ],
            areaCodes: [
                { "label": '英国 +44', "value": 44 },
                { "label": "大陆 +86", "value": 86 },
                { "label": '日本 +81', "value": 81 },
                { "label": '韩国 +82', "value": 82 },
            ],
            accountTypes:[
                { "label": '现货', "value": 1 },
                { "label": 'U本位合约 ', "value": 6 },
                { "label": '币本位合约', "value": 7 },
                { "label": '现货杠杆', "value": 10 }
            ],
            tradeTypes:[
                { "label": '现货', "trade_type": "SPOT","sign_type": "BTCUSDT","buy_way":false,"is_close":false},
                { "label": '现货杠杆', "trade_type": "MARGIN","sign_type": "BTCUSDT","buy_way":false,"is_close":false},
                { "label": 'U本位合约', "trade_type": "CONTRACT","sign_type": "BTCUSDT_UMCBL","buy_way":false,"is_close":false},
                { "label": '币本位合约', "trade_type": "CONTRACT","sign_type": "BTCUSD_DMCBL","buy_way":false,"is_close":false}
            ],
            envName: "test",
            activityTypes : Object,
            qaUser : util.getLoginName(),
            // qaUser : "hasaki",
        }
    },
    methods: {
        setEnv(val,user) {
            axios.defaults.headers['envData'] = val
            this.envName = val
            axios.defaults.headers['loginUser'] = user
        },
        record(){
            this.recordSend(this.envName,this.qaUser,"活动","")
        },
        recordSend(env,user,module,action){
            const data = {
                env: env,
                user: user,
                module: module,
                action: action
            }
            axios.post('/test/record', data)
        },
        getCountryName(val){
            for(let key in this.authCountrys){
                if(this.authCountrys[key].value === val){
                    return this.authCountrys[key].label
                }
            }
        },
    },
    async mounted() {
        // await this.setUser()
        // await this.setEnv()
        // this.getActivityTypes()
        // console.log(this.activityTypes)
    },
    async created() {
        // await this.setUser()
        // await this.setEnv()
        // this.getActivityTypes()
    }
}