function formatNumber(value) {
  return value.toLocaleString("vi-VN", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
}

function parseMoney(value) {
  if (!value) return 0;
  const cleaned = value.toString().replace(/\D/g, "");
  return cleaned ? parseFloat(cleaned) : 0;
}

function parseRate(value) {
  if (!value) return 0;
  return parseFloat(value.toString().replace(",", ".")) || 0;
}

function formatMoneyInput(input) {
  if (!input) return;
  var num = parseMoney(input.value);
  if (!num) {
    input.value = "";
    return;
  }
  input.value = formatNumber(num);
}

function recalcInterest(form) {
  if (!form) return;

  var pawnValueInput = form.querySelector("[name='pawn_value']");
  var rateInput = form.querySelector("[name='interest_rate']");
  var daysInput = form.querySelector("[name='duration_days']");
  var interestOutput = form.querySelector("[data-interest-output]");
  var totalOutput = form.querySelector("[data-total-output]");

  if (!pawnValueInput || !rateInput || !daysInput || !interestOutput || !totalOutput) {
    return;
  }

  var pawnValue = parseMoney(pawnValueInput.value);
  var rateMonthly = parseRate(rateInput.value);
  var days = parseInt(daysInput.value, 10) || 0;

  // Hiển thị tiền cầm với dấu chấm ngăn cách hàng nghìn
  formatMoneyInput(pawnValueInput);

  if (pawnValue <= 0 || rateMonthly <= 0 || days <= 0) {
    interestOutput.textContent = "0";
    totalOutput.textContent = "0";
    return;
  }

  var rateDaily = rateMonthly / 30 / 100;
  var interest = pawnValue * rateDaily * days;
  var total = pawnValue + interest;

  interestOutput.textContent = formatNumber(Math.round(interest));
  totalOutput.textContent = formatNumber(Math.round(total));
}

document.addEventListener("input", function (event) {
  var target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (!target.matches("[data-interest-input]")) return;

  var form = target.closest("form");
  recalcInterest(form);
});

document.addEventListener("DOMContentLoaded", function () {
  var forms = document.querySelectorAll("form[data-interest-form]");
  forms.forEach(function (form) {
    recalcInterest(form);
  });
});
