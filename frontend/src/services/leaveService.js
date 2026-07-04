export const leaveService = {
  async getLeaves() {
    return [
      { id: 1, employee: 'Asha Rao', type: 'Sick', startDate: '2026-07-10', endDate: '2026-07-12', status: 'Pending', remarks: 'Flu symptoms' },
      { id: 2, employee: 'Kiran Das', type: 'Paid', startDate: '2026-07-15', endDate: '2026-07-16', status: 'Approved', remarks: 'Family event' },
    ];
  },
};
