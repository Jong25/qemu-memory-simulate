#!/bin/bash

echo 0 > /sys/kernel/debug/tracing/events/kvmmmu/enable
echo 0 > /sys/kernel/debug/tracing/events/kvm/enable


events=(
		"kvm_mmu_pagetable_walk" "kvm_mmu_paging_element" "kvm_mmu_set_accessed_bit" "kvm_mmu_set_dirty_bit"
		"kvm_mmu_walker_error" "kvm_mmu_get_page" "kvm_mmu_sync_page" "kvm_mmu_unsync_page"
		"kvm_mmu_prepare_zap_page" "mark_mmio_spte" "handle_mmio_page_fault" "fast_page_fault"
		"kvm_mmu_zap_all_fast" "check_mmio_spte" "kvm_mmu_set_spte" "kvm_mmu_spte_requested"
		)
