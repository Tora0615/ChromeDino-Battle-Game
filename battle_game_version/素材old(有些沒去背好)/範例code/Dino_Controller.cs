using UnityEngine;
using System.Collections;


public class Dino_Controller : MonoBehaviour
{
    public GameObject Fire;  //技能   
    public GameObject Tornado;
    public GameObject Thunder;
    Animator _anim;
	public float MoveSpeed = 5f;
	public float JumpPower = 1600f;
	private Rigidbody2D m_Rigidbody2D;
	
	Vector3 Start_Scale;
    
    private float Direction; //宣告浮點變數:位置(用以判斷朝向何處)
    float timelost = 0; //計時變數宣告

    void Start ()
	{
		_anim = GetComponent<Animator> ();
		Start_Scale = transform.localScale;
		m_Rigidbody2D = GetComponent<Rigidbody2D>();
        
    }

	void Update ()
	{
        // ↓移動判定
        if (Input.GetKey (KeyCode.A) || Input.GetKey (KeyCode.D) ) { 	//判斷是否向左、向右按鍵是否被觸發			
																			
				_anim.SetBool ("Move", true);					        //如果是，move條件設為true										
				float xx = Input.GetAxisRaw ("Horizontal");             //偵測向左還向右移動(?
				if(Input.GetKey (KeyCode.D)) {					        //如果是按向右										
					transform.localScale = new Vector3 (Start_Scale.x, Start_Scale.y, Start_Scale.z);       //改變本體大小(X*1 / Y*1 / Z*1)
					transform.Translate (Vector3.right * xx * MoveSpeed * Time.deltaTime);                  //改變位置(向右*X數值*移動速度*持續時間)                  
                 }               
                else if(Input.GetKey (KeyCode.A)) {
					transform.localScale = new Vector3 (-Start_Scale.x, Start_Scale.y, Start_Scale.z);
					transform.Translate (Vector3.right * xx * MoveSpeed * Time.deltaTime);                                                                                                                                                           
                } 
		}
        else
        {
			_anim.SetBool ("Move", false);                                                                      
        }

        // ↓普通攻擊判定
        if (Input.GetKeyDown(KeyCode.H))    
        {
            //float xx = Input.GetAxisRaw("Horizontal");
            Direction = transform.localScale.x;
            if (Direction > 0)
            {           
                Vector3 pos = gameObject.transform.position + new Vector3(1.71f, 0.29f, 0);
                Instantiate(Fire, pos, Quaternion.Euler(0f, 0f, 0f));
            }
            else
            {
                Vector3 pos = gameObject.transform.position + new Vector3(-1.71f,0.29f, 0);
                Instantiate(Fire, pos, gameObject.transform.rotation);
            }
        }

        // ↓第二攻擊判定
        if (Input.GetKeyDown(KeyCode.J))
        {
            //float xx = Input.GetAxisRaw("Horizontal");
            Direction = transform.localScale.x;
            if (Direction > 0)
            {
                Vector3 pos = gameObject.transform.position + new Vector3(1.68f, 1.27f, 0);
                Instantiate(Tornado, pos, gameObject.transform.rotation);
            }
            else
            {
                Vector3 pos = gameObject.transform.position + new Vector3(-1.68f, 1.27f, 0);
                Instantiate(Tornado, pos, gameObject.transform.rotation);
            }
        }

        // ↓第三攻擊判定
        if (Input.GetKeyDown(KeyCode.K))
        {
            //float xx = Input.GetAxisRaw("Horizontal");
            Direction = transform.localScale.x;
            if (Direction > 0)
            {
                Vector3 pos = gameObject.transform.position + new Vector3(3.51f, 0f, 0);
                pos.y = 0.515f;
                Instantiate(Thunder, pos, gameObject.transform.rotation);
            }
            else
            {
                Vector3 pos = gameObject.transform.position + new Vector3(-3.51f, 0f, 0);
                pos.y = 0.515f;
                Instantiate(Thunder, pos, gameObject.transform.rotation);
            }
        }

        // ↓下落、蹲下判定
        if (Input.GetKey(KeyCode.S))
        {
            _anim.SetBool("Down", true);   //動畫布林值判斷                                                                 
            float yy = Input.GetAxisRaw("Vertical");
            //transform.localScale = new Vector3(Start_Scale.x, -Start_Scale.y, Start_Scale.z);  //會上下顛倒(有趣沒刪)
            transform.Translate(Vector3.up * yy *1.5f* MoveSpeed * Time.deltaTime);  //加速落下           
        }
        else
        {
            _anim.SetBool("Down", false);
        }

        // ↓跳躍判斷
        if (Input.GetKeyDown (KeyCode.W)|| Input.GetKeyDown(KeyCode.Space)) {		
			m_Rigidbody2D.AddForce(new Vector2(0f, JumpPower));
			//_anim.SetTrigger ("Jump");	(若有跳躍動畫可啟用)										
		}
        
        // ↓瞬間移動判定
        if (Input.GetKeyDown(KeyCode.L))   
        {
            if (Time.time - timelost < 0.5f) //0.5秒之内按下有效
            {
                _anim.SetTrigger("Fast move");  //觸發動畫Fast_Move
                Direction = transform.localScale.x;
                if (Input.GetKeyDown(KeyCode.L) && Direction<0)
                {
                    transform.position = gameObject.transform.position + new Vector3(-1.3f, 0f, 0);
                }
                if (Input.GetKeyDown(KeyCode.L) && Direction > 0)
                {
                    transform.position = gameObject.transform.position + new Vector3(1.3f, 0f, 0);
                }


            }

            timelost = Time.time;
        }
        
        
    }
}
