#define PT_MAX_FULL_LEVELS  4
#define PTE_PREFETCH_NUM    8
#define gfn_t u64
#define gpa_t u64
#define hpa_t u64
#define pt_element_t u64
#define KVM_PAGE_TRACK_MAX 1
#define KVM_NR_PAGE_SIZES 3
#define PT64_ROOT_MAX_LEVEL 5
#define KVM_MEM_SLOTS_NUM 512


struct x86_exception {
    u8 vector;
    bool error_code_valid;
    u16 error_code;
    bool nested_page_fault;
    u64 address; /* cr2 or nested page fault gpa */
    u8 async_page_fault;
};

struct guest_walker {
    int level;
    unsigned max_level;
    gfn_t table_gfn[PT_MAX_FULL_LEVELS];
    pt_element_t ptes[PT_MAX_FULL_LEVELS];
    pt_element_t prefetch_ptes[PTE_PREFETCH_NUM];
    gpa_t pte_gpa[PT_MAX_FULL_LEVELS];
    pt_element_t __user *ptep_user[PT_MAX_FULL_LEVELS];
    bool pte_writable[PT_MAX_FULL_LEVELS];
    unsigned pt_access;
    unsigned pte_access;
    gfn_t gfn;
    struct x86_exception fault;
};

/*
struct kvm_vcpu {
	struct kvm *kvm;
	struct preempt_notifier preempt_notifier;
	int cpu;
	int vcpu_id;
	int srcu_idx;
	int mode;
	u64 requests;
	unsigned long guest_debug;

	int pre_pcpu;
	struct list_head blocked_vcpu_list;

	struct mutex mutex;
	struct kvm_run *run;

	int guest_xcr0_loaded;
	struct swait_queue_head wq;
	struct pid __rcu *pid;
	int sigset_active;
	sigset_t sigset;
	struct kvm_vcpu_stat stat;
	unsigned int halt_poll_ns;
	bool valid_wakeup;

	int mmio_needed;
	int mmio_read_completed;
	int mmio_is_write;
	int mmio_cur_fragment;
	int mmio_nr_fragments;
	struct kvm_mmio_fragment mmio_fragments[KVM_MAX_MMIO_FRAGMENTS];

	struct {
		u32 queued;
		struct list_head queue;
		struct list_head done;
		spinlock_t lock;
	} async_pf;

	struct {
		bool in_spin_loop;
		bool dy_eligible;
	} spin_loop;

	bool preempted;
	bool ready;
	struct kvm_vcpu_arch arch;
	struct dentry *debugfs_dentry;
};

struct rsvd_bits_validate {
	u64 rsvd_bits_mask[2][PT64_ROOT_MAX_LEVEL];
	u64 bad_mt_xwr;
};

struct kvm_mmu {
	void (*set_cr3)(struct kvm_vcpu *vcpu, unsigned long root);
	unsigned long (*get_cr3)(struct kvm_vcpu *vcpu);
	u64 (*get_pdptr)(struct kvm_vcpu *vcpu, int index);
	int (*page_fault)(struct kvm_vcpu *vcpu, gva_t gva, u32 err,
			  bool prefault);
	void (*inject_page_fault)(struct kvm_vcpu *vcpu,
				  struct x86_exception *fault);
	gpa_t (*gva_to_gpa)(struct kvm_vcpu *vcpu, gva_t gva, u32 access,
			    struct x86_exception *exception);
	gpa_t (*translate_gpa)(struct kvm_vcpu *vcpu, gpa_t gpa, u32 access,
			       struct x86_exception *exception);
	int (*sync_page)(struct kvm_vcpu *vcpu,
			 struct kvm_mmu_page *sp);
	void (*invlpg)(struct kvm_vcpu *vcpu, gva_t gva, hpa_t root_hpa);
	void (*update_pte)(struct kvm_vcpu *vcpu, struct kvm_mmu_page *sp,
			   u64 *spte, const void *pte);
	hpa_t root_hpa;
	gpa_t root_cr3;
	union kvm_mmu_role mmu_role;
	u8 root_level;
	u8 shadow_root_level;
	u8 ept_ad;
	bool direct_map;
	struct kvm_mmu_root_info prev_roots[KVM_MMU_NUM_PREV_ROOTS];

	u8 permissions[16];

	u32 pkru_mask;

	u64 *pae_root;
	u64 *lm_root;

	struct rsvd_bits_validate shadow_zero_check;

	struct rsvd_bits_validate guest_rsvd_check;

	u8 last_nonleaf_level;

	bool nx;

	u64 pdptrs[4];
};
*/


struct kvm_lpage_info {
	int disallow_lpage;
};

struct kvm_rmap_head {
	unsigned long val;
};

struct kvm_arch_memory_slot {
	struct kvm_rmap_head *rmap[KVM_NR_PAGE_SIZES];
	struct kvm_lpage_info *lpage_info[KVM_NR_PAGE_SIZES - 1];
	unsigned short *gfn_track[KVM_PAGE_TRACK_MAX];
};

struct kvm_memory_slot {
	gfn_t base_gfn;
	unsigned long npages;
	unsigned long *dirty_bitmap;
	struct kvm_arch_memory_slot arch;
	unsigned long userspace_addr;
	u32 flags;
	short id;
};

struct kvm_memslots {
	u64 generation;
	struct kvm_memory_slot memslots[KVM_MEM_SLOTS_NUM];
	short id_to_index[KVM_MEM_SLOTS_NUM];
	atomic_t lru_slot;
	int used_slots;
};

struct kvm_userspace_memory_region {
	__u32 slot;
	__u32 flags;
	__u64 guest_phys_addr;
	__u64 memory_size; /* bytes */
	__u64 userspace_addr; /* start of the userspace allocated memory */
};
